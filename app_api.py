
import streamlit as st
import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import io

app = FastAPI()

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(content={"error": "Invalid file type"}, status_code=400)

    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    has_commande = "commande :" in text.lower()
    return {"text": text, "commande_detectee": has_commande}
