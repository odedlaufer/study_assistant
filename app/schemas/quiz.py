from typing import List

from pydantic import BaseModel


class Answer(BaseModel):
    question: str
    selected: str


class QuizSubmission(BaseModel):
    note_id: str
    answers: List[Answer]
