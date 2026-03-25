import express from "express";
import multer from "multer";
import { sendToAI } from "../services/aiService.js";

const router = express.Router();
const upload = multer({ storage: multer.memoryStorage() });

router.post("/predict", upload.single("file"), async (req, res, next) => {
    try {
        console.log("📥 Petición recibida");
        if (!req.file) {
            return res.status(400).json({ error: "No se envió archivo" });
        }

        if (!req.file.mimetype.startsWith("image/")) {
            return res.status(400).json({ error: "El archivo debe ser imagen" });
        }
        const result = await sendToAI(req.file);

        console.log("✅ Respuesta enviada");

        res.json(result);

    } catch (error) {
        next(error);
    }
});

export default router;