from transformers import pipeline


summarizer_pipeline = pipeline("summarization", model="t5-small", tokenizer="t5-small")


def summarize_text(text: str, max_length=150, min_length=30) -> str:
    text = "summarize: " + text.strip().replace("\n", " ")
    summary = summarizer_pipeline(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']  # type: ignore

