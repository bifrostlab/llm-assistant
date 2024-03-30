import time
import fitz
import gdown
import os


def download_pdf(url: str) -> str:
  if not os.path.exists("cache"):
    os.mkdir("cache")

  output_path = f"cache/{time.time()}.pdf"
  gdown.download(url, output_path, fuzzy=True)

  return output_path


def parse_pdf(pdf_path: str) -> str:
  with fitz.open(pdf_path) as pdf:
    text_list = []
    for page in pdf:
      text_list.append(page.get_text())
    text = "\n\n".join(text_list)

  return text
