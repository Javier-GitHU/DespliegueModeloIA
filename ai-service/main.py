
import io
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from ultralytics import YOLO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("YOLO_API")

log.info("🚀 Iniciando servicio de IA (YOLOv8)...")


MODEL_PATH = "models/best_yolov8.pt"
CONF_THRESHOLD = 0.4

try:
    log.info("Cargando modelo YOLO...")
    model = YOLO(MODEL_PATH)
    log.info("✅ Modelo cargado correctamente")
except Exception as e:
    log.error(f"❌ Error cargando el modelo: {e}")
    raise RuntimeError("No se pudo cargar el modelo")

def validate_image(file: UploadFile):
    """
    Validación de entrada
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

def preprocess_image(image_bytes: bytes) -> Image.Image:
    """
    Convierte bytes → imagen PIL
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return image
    except Exception:
        raise HTTPException(status_code=400, detail="Imagen inválida")

def run_inference(image: Image.Image) -> List[dict]:
    """
    Ejecuta predicción con YOLO
    """
    results = model.predict(image, conf=CONF_THRESHOLD, verbose=False)

    detections = []

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = model.names[cls_id]

        detections.append({
            "class": class_name,
            "confidence": confidence
        })

    return detections


app = FastAPI(title="SmartFridge AI Service")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint de predicción
    """
    try:
        log.info(f"📥 Petición recibida: {file.filename}")

        validate_image(file)

        contents = await file.read()

        image = preprocess_image(contents)

        detections = run_inference(image)

        log.info(f"✅ Predicción completada: {len(detections)} objetos detectados")

        return {
            "filename": file.filename,
            "detections": detections
        }

    except HTTPException as e:
        log.warning(f"⚠️ Error de cliente: {e.detail}")
        raise e

    except Exception as e:
        log.error(f"❌ Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")