from pydantic import BaseModel
from typing import List


class Answer(BaseModel):
    question: str
    selected: str


class QuizSubmission(BaseModel):
    note_id: str
    answers: List[Answer]
