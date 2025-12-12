import cv2
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

# === Configurações ===
modelo_path = "modelo_final.keras"
IMG_SIZE = (224, 224)
THRESHOLD = 0.42  # valor fixo do seu ROC
class_names = ["Benigno", "Maligno"]

# === Carrega modelo uma vez ===
modelo = load_model(modelo_path)

# === Inicializa FastAPI ===
app = FastAPI()

# === CORS para permitir React ===
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # ou ["*"] para liberar todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Funções auxiliares ===
def preprocess_cv_image(cv_img):
    img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

def inferir_imagem_array(img_array, threshold=THRESHOLD):
    pred = modelo.predict(img_array)[0][0]
    label = class_names[1] if pred >= threshold else class_names[0]
    return pred, label

# === Endpoint de predição ===
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="Arquivo inválido ou não é uma imagem.")

    img_array = preprocess_cv_image(img)
    prob, label = inferir_imagem_array(img_array)
    return {"probability": float(prob), "class_name": label}