import os
from .file_helpers import get_note_text
from .cache import get_cached, save_cache


def get_or_generate(note_id: str, kind: str, generator_fn):
    cache_path = f"app/storage/cache/{note_id}_{kind}.json"
    cached = get_cached(cache_path)
    if cached:
        return cached
    
    text = get_note_text(note_id)
    result = generator_fn(text)
    save_cache(cache_path, result)
    return result