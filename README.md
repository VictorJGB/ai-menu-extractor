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
