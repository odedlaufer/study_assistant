import os
import tempfile

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def uploaded_note_id():
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as temp:
        temp.write(
            "FastAPI is a modern, fast web framework for building APIs with Python."
        )
        temp_path = temp.name

    with open(temp_path, "rb") as f:
        response = client.post(
            "/upload", files={"file": (os.path.basename(temp_path), f, "text/plain")}
        )

    os.remove(temp_path)

    assert response.status_code == 200
    data = response.json()
    assert "note_id" in data
    return data["note_id"]


def test_upload_txt():
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as temp:
        temp.write(
            "FastAPI is a modern, fast web framework for building APIs with Python."
        )
        temp_path = temp.name

    with open(temp_path, "rb") as f:
        response = client.post(
            "/upload", files={"file": (os.path.basename(temp_path), f, "text/plain")}
        )

    os.remove(temp_path)
    assert response.status_code == 200
    assert "note_id" in response.json()


def test_get_summary(uploaded_note_id):
    res = client.get(f"/summary/{uploaded_note_id}")
    assert res.status_code == 200
    assert "summary" in res.json()


def test_get_flashcards(uploaded_note_id):
    res = client.get(f"/flashcards/{uploaded_note_id}")
    assert res.status_code == 200
    assert "flashcards" in res.json()


def test_get_quiz(uploaded_note_id):
    res = client.get(f"/quiz/{uploaded_note_id}")
    assert res.status_code == 200
    assert "quiz" in res.json()


def test_check_quiz(uploaded_note_id):
    quiz_res = client.get(f"/quiz/{uploaded_note_id}")
    assert quiz_res.status_code == 200
    quiz = quiz_res.json()["quiz"]
    assert len(quiz) > 0

    question = quiz[0]
    payload = {
        "note_id": uploaded_note_id,
        "answers": [
            {
                "question": question["question"],
                "selected": question["answer"],  # correct answer
            }
        ],
    }

    res = client.post("/check-quiz", json=payload)
    assert res.status_code == 200
    result = res.json()
    assert "score" in result
    assert result["score"].startswith("1/")
