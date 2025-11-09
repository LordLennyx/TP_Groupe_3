import express from "express";
import projectsRouter from "./routes/projects";

const app = express();
const PORT = 3004;

app.use(express.json());
app.use("/projects", projectsRouter);
// app.js ou index.js
app.get("/", (req, res) => {
  res.json({ message: "API REST TP opérationnelle" });
});

app.listen(PORT, () => {
  console.log(`? Serveur lancé sur http://localhost:${PORT}`);
});

