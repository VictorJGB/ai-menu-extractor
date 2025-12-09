import json
from pathlib import Path

from src.extractor import extract_pdf, extract_txt
from src.excel_generator import transform_products, generate_excel


def main():
    file_type = input("Escolha o tipo de arquivo (pdf/txt): ").strip().lower()

    if file_type not in ["pdf", "txt"]:
        print("Opção inválida.")
        return

    file_path = input("Digite o caminho do arquivo: ").strip()
    file_path = Path(file_path)

    if not file_path.exists():
        print("Arquivo não encontrado.")
        return

    if file_type == "pdf":
        print("Extraindo dados do PDF...")
        data = extract_pdf(file_path)
    else:
        print("Extraindo dados do TXT...")
        data = extract_txt(file_path)

    base_dir = Path("output")
    base_dir.mkdir(exist_ok=True)

    json_path = base_dir / "cardapio.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Arquivo JSON gerado com sucesso em:", json_path)

    products = transform_products(data)
    excel_path = base_dir / "cardapio.xlsx"
    generate_excel(products, excel_path)

    print("Arquivo Excel gerado com sucesso em:", excel_path)


if __name__ == "__main__":
    main()
