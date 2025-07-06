from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
import os
import shutil
from .services import parser, summarizer, flashcards, quiz
from .utils.file_helpers import get_note_text
from .schemas.quiz import QuizSubmission
from .utils.cache import get_cached, save_cache
from .utils.response_cache import get_or_generate


router = APIRouter()

NOTES_DIR = "app/storage/notes"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files")

    note_id = str(uuid4())
    file_path = os.path.join(NOTES_DIR, f"{note_id}_{file.filename}")

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed_text = parser.extract_text(file_path)

    with open(os.path.join(NOTES_DIR, f"{note_id}.txt"), 'w', encoding='utf-8') as f:
        f.write(parsed_text)

    return {"note_id": note_id, "message": "File uploaded and processed."}


@router.get("/summary/{note_id}")
def get_summary(note_id: str):
    result = get_or_generate(note_id, "summary", summarizer.summarize_text)
    return {"note_id": note_id, "summary": result}


@router.get("/flashcards/{note_id}")
def get_flashcards(note_id: str):
    result = get_or_generate(note_id, "flashcards", flashcards.generate_flashcards)
    return {"note_id": note_id, "flashcards": result}


@router.get("/quiz/{note_id}")
def get_quiz(note_id: str):
    result = get_or_generate(note_id, "quiz", quiz.generate_quiz)
    return {"note_id": note_id, "quiz": result}


@router.post("/check-quiz")
def check_quiz(submission: QuizSubmission):
    text = get_note_text(submission.note_id)
    quiz_data = quiz.generate_quiz(text)

    correct_map = {item["question"]: item["answer"] for item in quiz_data}
    results = []
    correct_count = 0

    for answer in submission.answers:
        correct_answer = correct_map.get(answer.question)

        if correct_answer is None:
            raise HTTPException(
                status_code=400,
                detail=f"Question not found in generated quiz: '{answer.question}"
            )
 
        is_correct = answer.selected.strip() == correct_answer.strip()  # type: ignore
        if is_correct:
            correct_count += 1
     
        results.append({
            "question": answer.question,
            "selected": answer.selected,
            "correct": is_correct,
            "answer": correct_answer
        })

    return {
        "note_id": submission.note_id,
        "results": results,
        "score": f"{correct_count}/{len(submission.answers)}"
    }
