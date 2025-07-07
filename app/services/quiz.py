import random
from difflib import SequenceMatcher

from transformers import pipeline

paraphrase_model = pipeline(
    "text2text-generation",
    model="Vamsi/T5_Paraphrase_Paws",
    tokenizer="Vamsi/T5_Paraphrase_Paws",
)


def is_similar(a, b, threshold=0.9):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold


def generate_quiz(text: str, num_questions: int = 3):
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]
    quiz = []

    for i in range(min(num_questions, len(sentences))):
        original = sentences[i]
        correct = original

        paraphrased_outputs = paraphrase_model(
            f"paraphrase: {correct} </s>",
            max_length=64,
            num_return_sequences=4,
            do_sample=True,
            top_k=50,
            top_p=0.95,
        )

        paraphrases = [
            output["generated_text"].strip()
            for output in paraphrased_outputs
            if not is_similar(output["generated_text"], correct)
        ]

        # Remove near duplicates within paraphrases too
        distinct = []
        for p in paraphrases:
            if all(not is_similar(p, existing) for existing in distinct):
                distinct.append(p)

        distractors = distinct[:2]

        # Pad with generic wrong answers if needed
        while len(distractors) < 2:
            distractors.append(
                random.choice(
                    [
                        "It is a JavaScript compiler.",
                        "It is used for database migration.",
                        "It is a CSS framework for styling.",
                        "It is a mobile app deployment tool.",
                    ]
                )
            )

        options = distractors + [correct]
        random.shuffle(options)

        quiz.append(
            {
                "question": f'What does this mean? "{original}"',
                "options": options,
                "answer": correct,
            }
        )

    return quiz
