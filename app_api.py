from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import fitz # PyMuPDF

app = FastAPI()

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
  if file.content_type != "application/pdf":
    return JSONResponse(content={"error": "Invalid file type"}, status_code=400)

  content = await file.read()
  doc = fitz.open(stream=content, filetype="pdf")
  text = "".join([page.get_text() for page in doc])
  doc.close()

  has_commande = "commande :" in text.lower()
  return {"text": text, "commande_detectee": has_commande}
