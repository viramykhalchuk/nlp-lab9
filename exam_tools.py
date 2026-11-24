import json
import random
import uuid
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "exam_results"
RESULTS_DIR.mkdir(exist_ok=True)


def load_json(filename):
    with open(BASE_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


class ExamTools:
    def __init__(self):
        self.email = None
        self.name = None
        self.topics = []
        self.topic_index = -1
        self.exam_id = None
        self.finished = False

    def start_exam(self, email: str, name: str) -> list[str]:
        if self.exam_id is not None:
            raise ValueError("Іспит вже розпочато.")

        email = email.strip().lower()
        name = name.strip()

        students = load_json("students.json")

        student = next(
            (
                student for student in students
                if student["email"].lower() == email
                and student["name"].casefold() == name.casefold()
            ),
            None
        )

        if student is None:
            raise ValueError(
                "Студента не знайдено. Перевірте ім'я та email."
            )

        self.email = student["email"]
        self.name = student["name"]
        self.topics = random.sample(load_json("topics.json"), 3)
        self.topic_index = -1
        self.exam_id = uuid.uuid4().hex
        self.finished = False

        self.save_result({
            "exam_id": self.exam_id,
            "name": self.name,
            "email": self.email,
            "topics": self.topics,
            "started_at": datetime.now().isoformat(timespec="seconds"),
            "status": "in_progress"
        })

        return self.topics

    def get_next_topic(self) -> str:
        if self.exam_id is None:
            raise ValueError("Іспит ще не розпочато.")

        if self.finished:
            raise ValueError("Іспит вже завершено.")

        if self.topic_index + 1 >= len(self.topics):
            return "NO_MORE_TOPICS"

        self.topic_index += 1
        return self.topics[self.topic_index]

    def end_exam(
        self, email: str, score: float, history: list[dict]
    ) -> None:
        if self.exam_id is None or self.finished:
            raise ValueError("Немає активного іспиту.")

        if email.strip().lower() != self.email.lower():
            raise ValueError("Email не відповідає активному іспиту.")

        if self.topic_index != len(self.topics) - 1:
            raise ValueError("Не всі теми пройдено.")

        if not 0 <= score <= 10:
            raise ValueError("Оцінка повинна бути від 0 до 10.")

        path = RESULTS_DIR / f"{self.exam_id}.json"

        with open(path, encoding="utf-8") as file:
            result = json.load(file)

        result.update({
            "score": round(score, 2),
            "history": history,
            "finished_at": datetime.now().isoformat(timespec="seconds"),
            "status": "completed"
        })

        self.save_result(result)
        self.finished = True

    def save_result(self, result):
        path = RESULTS_DIR / f"{self.exam_id}.json"

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                result,
                file,
                ensure_ascii=False,
                indent=2
            )