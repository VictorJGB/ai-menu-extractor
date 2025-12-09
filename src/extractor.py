import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()


def config_gemini():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")

    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-2.5-flash")


def extract_pdf(pdf_path) -> str:
    model = config_gemini()

    prompt = """
    Você é um extrator de dados. Extraia do texto abaixo as categorias, os produtos e seus preços.
    
    Retorne **somente JSON puro**, sem explicações.
    NÃO use markdown.
    NÃO use ```json.
    NÃO coloque nenhum texto antes ou depois.
    O JSON deve começar com [ e terminar com ].
    
    Formato obrigadorio:
    [
      {
        "categoria": "nome",
        "itens": [
          { "nome": "produto", "preco": 0.00 }
        ]
      }
    ]
    """

    file = genai.upload_file(pdf_path)
    response = model.generate_content([prompt, file])
    return json.loads(response.text)


def extract_txt(txt_path):
    categories = []
    current_category = None

    with open(txt_path, "r", encoding="utf-8") as file:
        for line in file:
            current_line = line.strip()
            if not current_line:
                continue

            # New category
            if "R$" not in current_line:
                current_category = {"categoria": current_line, "itens": []}

                categories.append(current_category)
                continue

            # Menu items
            name_part, price_part = current_line.rsplit("R$", 1)
            name = name_part.strip()
            price = float(price_part.replace(",", ".").strip())

            current_category["itens"].append({"nome": name, "preco": price})

    return categories
