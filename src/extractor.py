import google.generativeai as genai
import re


def config_gemini(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def extrair_dados(model, text: str) -> str:
    prompt = f"""
    Você é um extrator de dados. Extraia do texto abaixo as categorias, os produtos e seus preços.
    
    Retorne **somente JSON puro**, sem explicações.
    NÃO use markdown.
    NÃO use ```json.
    NÃO coloque nenhum texto antes ou depois.
    O JSON deve começar com [ e terminar com ].
    
    Formato obrigadorio:

    [
      {{
        "categoria": "nome_da_categoria",
        "itens": [
          {{ "nome": "produto", "preco": 0.00 }}
        ]
      }}
    ]

    Texto:
    ---------------------
    {text}
    ---------------------
    """

    response = model.generate_content(prompt)
    return response.text
