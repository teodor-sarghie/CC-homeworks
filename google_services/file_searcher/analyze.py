import os
import tempfile
import shutil

import PyPDF2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from dotenv import load_dotenv
from google.cloud import language_v1
import pdfplumber

load_dotenv()


def classify_sentiment(score):
    if score <= -0.75:
        return "very negative"
    elif score <= -0.25:
        return "negative"
    elif score < 0.25:
        return "neutral"
    elif score < 0.75:
        return "positive"
    else:
        return "very positive"


def classify_magnitude(magnitude):
    if magnitude == 0:
        return "no emotional content"
    elif magnitude < 2.0:
        return "emotional content"
    elif magnitude < 5.0:
        return "strong emotional content"
    else:
        return "very emotional content"


def extract_sentiment(text):
    client = language_v1.LanguageServiceClient()

    document = language_v1.types.Document(
        content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
    )
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    return f"{classify_sentiment(sentiment.score)}, {classify_sentiment(sentiment.magnitude)}"


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    return text


def classify_text(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    request = language_v1.ClassifyTextRequest(
        document=document,
    )
    response = client.classify_text(request=request)
    return ",".join([category.name for category in response.categories])


def save_temporary_file(stream_generator, filename):
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, filename)

    with open(temp_file_path, "wb") as temp_file:
        for chunk in stream_generator():
            temp_file.write(chunk)

    final_path = default_storage.save(
        f"temp/{filename}.pdf", ContentFile(open(temp_file_path, "rb").read())
    )

    shutil.rmtree(temp_dir)
    return final_path


if __name__ == "__main__":
    pdf_path = "/home/tudor/UAIC/AN3/Sem2/Calculus/lab/lab4/4/smre.pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    print(pdf_text)
    categories = classify_text(pdf_text)
    sentiment = extract_sentiment(pdf_text)
    print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")

    sentiment_category = classify_sentiment(sentiment.score)
    magnitude_category = classify_magnitude(sentiment.magnitude)

    print(sentiment_category, magnitude_category)
