import os
from io import BytesIO

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from typing import Union, Annotated

from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling_core.types.io import DocumentStream
from fastapi import FastAPI, File, UploadFile, Form

app = FastAPI()

artifacts_path =  StandardPdfPipeline.download_models_hf(
    local_dir = os.path.join(os.getcwd(), "model_artifacts"),
)
print(artifacts_path)
pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
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
    print("Converting...")
    result = converter.convert(source)
    print("Conversion done.")
    resultData = result.document.export_to_markdown()
    del source
    del result
    del buf
    return {"result": resultData}


