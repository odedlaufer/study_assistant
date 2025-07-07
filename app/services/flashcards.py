import re

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

MODEL_NAME = "mrm8488/t5-base-finetuned-question-generation-ap"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

qg_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)


def clean_text(text: str) -> list[str]:
    sentence = re.split(r"(?<=[.?!])\s+", text.strip())
    return [
        s.strip()
        for s in sentence
        if len(s.strip()) > 30 and len(s.strip().split()) > 5
    ]


def generate_flashcards(text: str, max_questions: int = 5):
    sentences = text.strip().split(".")
    flashcards = []

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20 and len(flashcards) < max_questions:
            result = qg_pipeline(sentence)
            question = result[0]["generated_text"]  # type: ignore
            flashcards.append({"question": question, "answer": sentence})

    return flashcards
