import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def config_gemini():
    key = os.getenv("GEMINI_API_KEY")

    if not key:
        raise ValueError(
            "GEMINI_API_KEY não encontrada nas variáveis de ambiente."
        )

    return genai.Client(api_key=key)


def extract_pdf(pdf_path):
    client = config_gemini()

    prompt = """
    Você é um extrator de dados. Extraia do texto abaixo as categorias,
    os produtos e seus preços.

    Retorne somente JSON puro, sem explicações.
    NÃO use markdown.
    NÃO use ```json.
    NÃO coloque nenhum texto antes ou depois.
    O JSON deve começar com [ e terminar com ].

    Formato obrigatório:
    [
      {
        "categoria": "nome",
        "itens": [
          { "nome": "produto", "preco": 0.00 }
        ]
      }
    ]
    """

    file = client.files.upload(file=pdf_path)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[prompt, file],
    )

    return json.loads(response.text)


def extract_txt(txt_path):
    categories = []
    current_category = None

    with open(txt_path, "r", encoding="utf-8") as file:
        for line in file:
            current_line = line.strip()

            if not current_line:
                continue

            if "R$" not in current_line:
                current_category = {
                    "categoria": current_line,
                    "itens": []
                }

                categories.append(current_category)
                continue

            name_part, price_part = current_line.rsplit("R$", 1)

            name = name_part.strip()
            price = float(
                price_part.replace(",", ".").strip()
            )

            current_category["itens"].append({
                "nome": name,
                "preco": price
            })

    return categories