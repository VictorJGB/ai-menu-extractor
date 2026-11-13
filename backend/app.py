"""HTTP adapter for the existing menu extraction and Excel pipeline."""

import logging
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from starlette.concurrency import run_in_threadpool

from backend.services.excel_generator import generate_excel, transform_products
from backend.services.extractor import extract_pdf, extract_txt

app = FastAPI(title="AI Menu Extractor")
logger = logging.getLogger(__name__)
# Leave room for multipart headers under Vercel's 4.5 MB request limit.
MAX_SIZE = 4 * 1024 * 1024


def convert(content: bytes, suffix: str) -> bytes:
    with TemporaryDirectory(prefix="menu-extractor-") as directory:
        source = Path(directory) / f"cardapio{suffix}"
        source.write_bytes(content)
        # Gemini supports both PDF and JPEG files through the same upload API.
        data = extract_txt(source) if suffix == ".txt" else extract_pdf(source)
        products = transform_products(data)
        if not products:
            raise ValueError("Nenhum produto encontrado. Verifique o conteúdo do cardápio.")
        destination = Path(directory) / "cardapio.xlsx"
        generate_excel(products, destination)
        return destination.read_bytes()


@app.post("/api/extract")
async def extract(file: UploadFile):
    try:
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in {".pdf", ".jpg", ".jpeg", ".txt"}:
            raise HTTPException(400, "Envie um arquivo PDF, JPG ou TXT.")
        content = await file.read(MAX_SIZE + 1)
        if len(content) > MAX_SIZE:
            raise HTTPException(413, "O arquivo deve ter no máximo 4 MB.")
        if not content:
            raise HTTPException(400, "O arquivo está vazio.")
        if suffix == ".pdf" and not content.startswith(b"%PDF-"):
            raise HTTPException(400, "O arquivo não é um PDF válido.")
        if suffix in {".jpg", ".jpeg"} and not content.startswith(b"\xff\xd8\xff"):
            raise HTTPException(400, "O arquivo não é uma imagem JPG válida.")
        result = await run_in_threadpool(convert, content, suffix)
        return StreamingResponse(
            BytesIO(result),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": 'attachment; filename="cardapio.xlsx"'},
        )
    except HTTPException:
        raise
    except (ValueError, UnicodeError) as exc:
        message = str(exc) if suffix == ".txt" else "Não foi possível identificar produtos. Verifique o arquivo e tente novamente."
        raise HTTPException(422, message) from exc
    except Exception as exc:
        logger.exception("Menu conversion failed")
        raise HTTPException(502, "Não foi possível processar o cardápio. Verifique a configuração do Gemini no servidor e tente novamente.") from exc
    finally:
        await file.close()
