import os
import gradio as gr
from agent import ExamAgent
from openai import (
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APIStatusError
)


GREETING = (
    "Вітаю! Я ваш AI-екзаменатор з курсу NLP. "
    "Вкажіть, будь ласка, ваше ім'я та email."
)


def send_message(message, api_key, chat_history, agent):
    if not message.strip():
        return "", chat_history, agent, "", ""

    if not api_key.strip():
        gr.Warning("Спочатку введіть OpenRouter API key.")
        return message, chat_history, agent, "", ""

    if agent is None:
        agent = ExamAgent()

    if agent.tools.finished:
        gr.Warning("Іспит завершено. Почніть новий іспит.")
        return "", chat_history, agent, "\n".join(
            agent.models
        ), "\n".join(agent.tool_log)

    try:
        answer = agent.reply(
            message.strip(),
            api_key.strip()
        )

    except AuthenticationError:
        answer = "Некоректний API-ключ. Перевірте його."

    except RateLimitError:
        answer = (
            "Досягнуто ліміту безкоштовних запитів. "
            "Спробуйте пізніше."
        )

    except APIConnectionError:
        answer = "Помилка підключення до OpenRouter."

    except APIStatusError as error:
        answer = f"Помилка API. Код: {error.status_code}."

    except Exception as error:
        answer = f"Помилка: {type(error).__name__}."

    chat_history = chat_history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer}
    ]

    models = "\n".join(agent.models)
    tools = "\n".join(agent.tool_log)

    return "", chat_history, agent, models, tools


def reset_exam():
    return [
        {"role": "assistant", "content": GREETING}
    ], None, "", "", ""


with gr.Blocks(
    theme=gr.themes.Soft(),
    title="AI Examiner Agent"
) as demo:

    agent_state = gr.State(None)

    gr.Markdown(
        """
        # AI Examiner Agent

        Інтелектуальний агент для проведення
        іспиту з курсу NLP.

        Агент аналізує відповіді студента,
        ставить додаткові запитання та формує
        підсумкову оцінку від 0 до 10.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            api_key = gr.Textbox(
                label="OpenRouter API Key",
                type="password",
                placeholder="sk-or-v1-..."
            )

            gr.Markdown(
                """
                ### Демонстраційний студент

                **Name:** Test Student

                **Email:** student@example.com

                Використовуйте демонстраційні дані.
                """
            )

            reset_button = gr.Button(
                "Новий іспит"
            )

            model_info = gr.Textbox(
                label="Використані LLM-моделі",
                interactive=False,
                lines=3
            )

            tool_info = gr.Textbox(
                label="Виклики інструментів агента",
                interactive=False,
                lines=6
            )

        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                value=[
                    {
                        "role": "assistant",
                        "content": GREETING
                    }
                ],
                type="messages",
                height=500,
                label="Діалог зі студентом"
            )

            message = gr.Textbox(
                placeholder="Введіть вашу відповідь...",
                label="Повідомлення",
                lines=2
            )

            send_button = gr.Button(
                "Надіслати",
                variant="primary"
            )

    inputs = [
        message,
        api_key,
        chatbot,
        agent_state
    ]

    outputs = [
        message,
        chatbot,
        agent_state,
        model_info,
        tool_info
    ]

    send_button.click(
        send_message,
        inputs=inputs,
        outputs=outputs
    )

    message.submit(
        send_message,
        inputs=inputs,
        outputs=outputs
    )

    reset_button.click(
        reset_exam,
        outputs=[
            chatbot,
            agent_state,
            message,
            model_info,
            tool_info
        ]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.queue(default_concurrency_limit=1).launch(
        server_name="0.0.0.0",
        server_port=port
    )
