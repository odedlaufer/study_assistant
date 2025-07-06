import os
from fastapi import HTTPException

NOTES_DIR = "app/storage/notes"


def get_note_text(note_id: str) -> str:
    text_path = os.path.join(NOTES_DIR, f"{note_id}.txt")

    if not os.path.exists(text_path):
        raise HTTPException(status_code=404, detail="Note not found.")

    with open(text_path, 'r', encoding='utf-8') as f:
        return f.read()
