---
title: AI Examiner Agent
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.50.0
python_version: "3.12"
app_file: app.py
pinned: false
---
# AI Examiner Agent

## Опис проєкту

AI Examiner Agent — інтелектуальний агент для проведення іспиту з курсу обробки мови методами штучного інтелекту.

Агент перевіряє дані студента, випадково обирає три теми з NLP, аналізує відповіді, ставить уточнювальні запитання, формує оцінку від 0 до 10 та надає індивідуальні рекомендації.

## Інструменти агента

- start_exam(email, name) — перевірка студента та вибір тем.
- get_next_topic() — отримання наступної теми.
- end_exam(email, score, history) — збереження результатів іспиту.

## Технології

- Python
- Gradio
- OpenRouter API
- LLM Tool Calling
- JSON

## Запуск проєкту

Встановлення залежностей:

```bash
pip install -r requirements.txt
```

Запуск програми:

```bash
python app.py
```

Відкрити у браузері http://127.0.0.1:7860.

Для роботи агента необхідно ввести власний OpenRouter API Key у відповідне поле вебінтерфейсу.

## Демонстраційний студент

Name: Test Student

Email: student@example.com

## Збереження результатів

Результати та історія діалогів зберігаються у JSON-файлах у директорії exam_results.

## Мовна модель

Використовується безкоштовний маршрутизатор openrouter/free. Назви фактично використаних моделей відображаються у вебінтерфейсі.