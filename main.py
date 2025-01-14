import os
from io import BytesIO

from docling.document_converter import DocumentConverter
from typing import Union, Annotated

from docling_core.types.io import DocumentStream
from fastapi import FastAPI, File, UploadFile, Form

app = FastAPI()


#receive multipart form data
@app.post("/convert")
async def convert(
    token: Annotated[str, Form()],
    file: UploadFile,
):
    if token != os.environ.get("API_TOKEN"):
        return {"error": "Invalid token"}

    buf = BytesIO(file.file.read())
    source = DocumentStream(name=file.filename, stream=buf)
    converter = DocumentConverter()
    print("Converting...")
    result = converter.convert(source)
    print("Conversion done.")
    resultData = result.document.export_to_markdown()
    return {"result": resultData}


