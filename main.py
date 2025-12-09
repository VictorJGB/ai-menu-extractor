import os
import json
from dotenv import load_dotenv
from pathlib import Path

from src.pdf_reader import read_pdf
from src.extractor import config_gemini, extrair_dados
from src.excel_generator import carregar_json, transformar_produtos, gerar_excel


def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

    pdf_path = "data/cardapio.pdf"

    print("Lendo o arquivo PDF...")
    pdf_text = read_pdf(pdf_path)

    print("Configurando o modelo Gemini...")
    model = config_gemini(api_key)

    print("Extraindo dados do texto...")
    json_data = extrair_dados(model, pdf_text)

    print("Salvando resultados...")
    with open("output/cardapio.json", "w", encoding="utf-8") as f:
        f.write(json_data)

    print("Cardápio verificado!")

    base_dir = Path("output")
    base_dir.mkdir(exist_ok=True)

    caminho_json = base_dir / "cardapio.json"
    caminho_excel = base_dir / "cardapio.xlsx"

    print("Gerando arquivo Excel...")
    dados = carregar_json(caminho_json)
    produtos_transformados = transformar_produtos(dados)
    gerar_excel(produtos_transformados, caminho_excel)

    print("Arquivo Excel gerado com sucesso em:", caminho_excel)


if __name__ == "__main__":
    main()
