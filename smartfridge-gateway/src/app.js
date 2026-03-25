
import express from "express";
import morgan from "morgan";
import predictionRoutes from "./controllers/predictionController.js";

const app = express();

// Logging automático
app.use(morgan("dev"));

// Rutas
app.use("/api", predictionRoutes);

// Manejo de errores global
app.use((err, req, res, next) => {
    console.error("❌ Error:", err.message);
    res.status(500).json({ error: "Error interno del servidor" });
});

const PORT = 3000;

app.listen(PORT, () => {
    console.log(`🚀 Gateway corriendo en http://localhost:${PORT}`);
});