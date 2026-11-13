import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from openpyxl import load_workbook

from api.extract import app
from backend.app import MAX_SIZE
from backend.services.excel_generator import columns_order


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_template_preserves_excel_contract(self):
        template = Path(__file__).resolve().parents[1] / "frontend/public/modelo-cardapio.txt"
        response = self.client.post(
            "/api/extract", files={"file": ("menu.txt", template.read_bytes())}
        )
        self.assertEqual(response.status_code, 200)
        rows = list(load_workbook(BytesIO(response.content)).active.values)
        self.assertEqual(list(rows[0]), columns_order)
        self.assertEqual(rows[1], ("PRODUTO", 1, "CATEGORIA", "padrão", "0000.00.00", 0, 10))
        self.assertEqual(len(rows), 6)
        self.assertEqual([row[1] for row in rows[1:]], list(range(1, 6)))

    def test_invalid_uploads(self):
        for name, content, status in [
            ("bad.txt", b"Produto R$10,00", 422),
            ("bad.txt", b"Categoria\nProduto R$abc", 422),
            ("empty.txt", b"", 400),
            ("bad.csv", b"x", 400),
            ("bad.jpg", b"bad", 400),
            ("bad.pdf", b"bad", 400),
            ("big.txt", b"x" * (MAX_SIZE + 1), 413),
        ]:
            with self.subTest(name=name, status=status):
                response = self.client.post("/api/extract", files={"file": (name, content)})
                self.assertEqual(response.status_code, status)

    @patch("backend.app.extract_pdf")
    def test_pdf_and_jpg_use_existing_pipeline(self, extract):
        extract.return_value = [{"categoria": "Bebidas", "itens": [{"nome": "Suco", "preco": 10}]}]
        for name, content in [("menu.pdf", b"%PDF-test"), ("menu.jpg", b"\xff\xd8\xfftest")]:
            with self.subTest(name=name):
                response = self.client.post("/api/extract", files={"file": (name, content)})
                self.assertEqual(response.status_code, 200)
                rows = list(load_workbook(BytesIO(response.content)).active.values)
                self.assertEqual(rows[1][0], "Suco")
        self.assertEqual(extract.call_count, 2)


if __name__ == "__main__":
    unittest.main()
