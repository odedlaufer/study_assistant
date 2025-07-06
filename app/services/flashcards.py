from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "mrm8488/t5-base-finetuned-question-generation-ap"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, trust_remote_code=True)


qg_pipeline = pipeline("text2text-generation",
                       model=model,
                       tokenizer=tokenizer)


def generate_flashcards(text: str, max_questions: int = 5):
    sentences = text.strip().split(".")
    flashcards = []

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20 and len(flashcards) < max_questions:
            result = qg_pipeline(sentence)
            question = result[0]["generated_text"]  # type: ignore
            flashcards.append({"question": question,
                               "answer": sentence})

    return flashcards
