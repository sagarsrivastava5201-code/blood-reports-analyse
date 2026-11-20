"""Blood report extraction + analysis for HealthLens."""
import pdfplumber
from google.genai import types
from chatbot import generate

ANALYSIS_PROMPT = """You are analysing a blood test report. Reply in simple, easy-to-understand
English. Avoid heavy medical jargon; if you use a medical term, explain it in plain words.

Use exactly this markdown structure:

## 📋 Summary
2-3 lines overall picture.

## 🧪 Test Results
A markdown table with columns: Test | Your Value | Normal Range | Status
Status must be one of: ✅ Normal, ⬆️ High, ⬇️ Low.

## ⚠️ Important Findings
Bullet list of abnormal values: what it may mean in simple words and common causes.

## 🥗 General Lifestyle Tips
3-5 practical diet/lifestyle tips related to the findings.

## 👨‍⚕️ When to See a Doctor
When the user should consult a doctor.

Rules: Do not diagnose. Do not suggest medicines. If a value or range is not
readable in the report, write "N/A" instead of guessing. If this is not a blood
report, say so politely."""


def extract_pdf_text(file) -> str:
    """Extract text (and tables) from an uploaded PDF."""
    parts = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            parts.append(text)
    return "\n".join(parts).strip()


def analyze_report(file, file_type: str) -> str:
    """Analyse an uploaded report (PDF or image) and return markdown."""
    if file_type == "application/pdf":
        text = extract_pdf_text(file)
        if not text:
            raise ValueError(
                "No text found in this PDF (it may be a scanned copy). "
                "Please upload a photo or screenshot (PNG/JPG) of the report instead."
            )
        contents = f"{ANALYSIS_PROMPT}\n\n--- REPORT TEXT ---\n{text}"
    else:
        contents = [
            types.Part.from_bytes(data=file.read(), mime_type=file_type),
            ANALYSIS_PROMPT,
        ]

    return generate(contents, max_tokens=6000)