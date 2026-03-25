import axios from "axios";
import FormData from "form-data";

const AI_URL = "http://ai-service:8000/predict";

export const sendToAI = async (file) => {
    try {
        const formData = new FormData();

        formData.append("file", file.buffer, {
            filename: file.originalname,
            contentType: file.mimetype
        });

        const response = await axios.post(AI_URL, formData, {
            headers: formData.getHeaders()
        });

        return response.data;

    } catch (error) {
        console.error("❌ Error comunicando con IA:", error.message);
        throw new Error("Error en servicio de IA");
    }
};