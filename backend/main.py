from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from models import TextInput
from storage import InputStorage, LayoutStorage

app = FastAPI()
input_storage = InputStorage()
layout_storage = LayoutStorage()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretório para salvar arquivos
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Criar um objeto TextInput e salvar
    text_input = TextInput(text=text, filename=file.filename)
    input_storage.save_input(text_input)

    # Atualizar os contadores de caracteres, bigramas e trigramas
    layout_storage.update_character_count(text_input.character_count)
    layout_storage.update_bigram_count(text_input.bigram_count)
    layout_storage.update_trigram_count(text_input.trigram_count)

    # Atualizar a matrix do layout
    layout_storage.update_matrix()

    return JSONResponse(content={"message": "Arquivo processado!", "data": text_input.to_dict(), "filename": file.filename}, status_code=200)

@app.get("/inputs/")
def get_inputs():
    return input_storage.get_inputs()

@app.get("/layout/")
def get_layout():
    return layout_storage.get_layout()