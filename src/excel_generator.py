import json
import pandas as pd


ordem_colunas = [
    "Nome",
    "Referência",
    "Categoria nível 1",
    "Marca",
    "NCM",
    "Controla estoque",
    "Preço de venda",
]


def carregar_json(caminho_json):
    with open(caminho_json, "r", encoding="utf-8") as f:
        return json.load(f)


def transformar_produtos(dados):
    produtos_transformados = []
    referencia = 1  # inicia contador

    for categoria in dados:
        categoria_nome = categoria.get("categoria", "")

        for item in categoria.get("itens", []):
            produtos_transformados.append(
                {
                    "Nome": item.get("nome", ""),
                    "Referência": referencia,
                    "Categoria nível 1": categoria_nome,
                    "Marca": "padrão",
                    "NCM": "0000.00.00",
                    "Controla estoque": 0,
                    "Preço de venda": item.get("preco", 0),
                }
            )
            referencia += 1

    return produtos_transformados


def gerar_excel(produtos, caminho_excel):
    df = pd.DataFrame(produtos)
    df = df[ordem_colunas]  # garantir ordem
    df.to_excel(caminho_excel, index=False)
