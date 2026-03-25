
import express from "express";
import morgan from "morgan";
import predictionRoutes from "./controllers/predictionController.js";

const app = express();

app.use(morgan("dev"));


app.use("/api", predictionRoutes);

app.use((err, req, res, next) => {
    console.error("❌ Error:", err.message);
    res.status(500).json({ error: "Error interno del servidor" });
});

const PORT = 3000;

app.listen(PORT, () => {
    console.log(`🚀 Gateway corriendo en http://localhost:${PORT}`);
});