import pandas as pd


columns_order = [
    "Nome",
    "Referência",
    "Categoria nível 1",
    "Marca",
    "NCM",
    "Controla estoque",
    "Preço de venda",
]


def transform_products(data):
    transformed_products = []
    reference = 1

    for category in data:
        category_name = category.get("categoria", "")

        for item in category.get("itens", []):
            transformed_products.append(
                {
                    "Nome": item.get("nome", ""),
                    "Referência": reference,
                    "Categoria nível 1": category_name,
                    "Marca": "padrão",
                    "NCM": "0000.00.00",
                    "Controla estoque": 0,
                    "Preço de venda": item.get("preco", 0),
                }
            )
            reference += 1

    return transformed_products


def generate_excel(products, excel_path):
    df = pd.DataFrame(products)
    df = df[columns_order]
    df.to_excel(excel_path, index=False)
