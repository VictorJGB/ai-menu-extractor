<a name="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#fonts">Fonts</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

This project its an Gemini AI PDP/TEXT menu extractor made with python. Your goal its to automate the extraction and organization of product data from PDF and text files. It processes raw inputs, structures the information, and generates a standardized Excel (.xlsx) spreadsheet containing product name, reference, category, pricing, and other key attributes. This way we can streamline catalog creation and data migration workflows by providing an efficient, reproducible, and extensible data-processing pipeline. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)
- ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

- Python v3.11.9+ ([Download Python](https://www.python.org/downloads/))

- pip
  ```sh
  python -m pip install --upgrade pip
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/VictorJGB/ai-menu-extractor
   ```
2. Install Packages
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

### Deploy na Vercel

O frontend e a API são publicados juntos, no mesmo domínio. Importe este
repositório na Vercel, mantenha **Root Directory** na raiz (`.`) e
**Framework Preset** em **Other**. O `vercel.json` já define instalação,
build, saída estática e função Python. Cadastre `GEMINI_API_KEY` nas variáveis
de ambiente de Production e Preview e faça o deploy.

### Interface web (React + TypeScript)

Para iniciar frontend e backend juntos, instale as dependências do workspace
na raiz (uma vez) e execute:

```powershell
corepack.cmd pnpm install
corepack.cmd pnpm run dev
```

É necessário ter o ambiente Python `.venv` com `requirements.txt` instalado,
conforme os comandos abaixo. Acesse `http://localhost:5173`; a API usa a porta
8000. Use `Ctrl+C` para encerrar. Se um dos processos encerrar, o outro também
será encerrado.

Para iniciar cada processo separadamente, na raiz:

```powershell
corepack.cmd pnpm run dev:frontend
corepack.cmd pnpm run dev:backend
```

A interface em `frontend/` usa Vite, Tailwind CSS, componentes shadcn/ui e Biome.
Aceita um PDF, JPG/JPEG ou TXT por vez, com até 4 MB, e oferece download de
`cardapio.xlsx`. PDF e JPG usam o Gemini e exigem `GEMINI_API_KEY` no `.env`
do backend. TXT é processado localmente, sem chamada à IA. A chave nunca é
enviada ao navegador.

Na raiz, instale as dependências e inicie a API:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Em outro terminal, inicie o frontend:

```powershell
cd frontend
corepack.cmd pnpm run dev
```

Acesse `http://localhost:5173`. O proxy do Vite encaminha `/api` para a API
em `http://127.0.0.1:8000`. Para produção, sirva `frontend/dist` e encaminhe
`/api` para o backend no mesmo domínio.

```powershell
cd frontend
corepack.cmd pnpm run check
corepack.cmd pnpm run build
```

Para executar os testes da API, na raiz:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

O TXT deve ser salvo em UTF-8, com a categoria antes dos produtos e os preços
com duas casas decimais:

```text
CATEGORIA
PRODUTO R$10,00
```

O botão **Baixar modelo TXT** disponibiliza
[`modelo-cardapio.txt`](frontend/public/modelo-cardapio.txt).
A API reutiliza `transform_products` e `generate_excel`, em `backend/services/`, mantendo a ordem das
colunas: Nome, Referência, Categoria nível 1, Marca, NCM, Controla estoque e
Preço de venda. Mantém também referências sequenciais, marca `padrão`, NCM
`0000.00.00` e controle de estoque `0`. Os arquivos de cada conversão são
temporários e não sobrescrevem os arquivos existentes em `output/`.

### Interface de terminal

Before all, make sure that you have a <code>.env</code> file with your <code>GEMINI_API_KEY</code> value.
```sh
e.g. GEMINI_API_KEY=SomeApIKeYValue
```
Don't know how to generate the API key? See more on: [Google AI Studio](https://aistudio.google.com/).

On the project folder, run

```sh
python main.py
```
Then, choose the file type you want to extract the menu
```sh
pdf or txt
```
After that, paste the file path so that the system can read it
```sh
e.g. C:\Users\User\Documents\menu.pdf
```
And that's it, the system its going to read the file, extract its information and create a file name <code>cardapio.xlsx</code> inside the <code>output</code> folder.

OBS: If you choose the <code>txt</code> file type, be sure that the file is following the format bellow, otherwise, it going tho throw an error.
  ```sh
  category
    product 01 R$price
    product 02 R$price

  category 02
    product 01 R$price
    product 02 R$price

  ...
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

- <a href = "mailto:victorgb.dev@gmail.com" target="_blank"><img src="https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white" ></a>

- <a href="https://www.linkedin.com/in/jerry-dev-084793203" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" ></a>

- <a href="https://instagram.com/_jerryGB" target="_blank"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Fonts -->

## Fonts

- [badges](https://github.com/Ileriayo/markdown-badges)

## Author

<a href="https://github.com/VictorJGB">
  <img width="150" height="150" src="https://user-images.githubusercontent.com/62398638/226929073-2c757280-6acf-4641-9fc1-bd7bb1f0485c.jpeg" />
<a/>
