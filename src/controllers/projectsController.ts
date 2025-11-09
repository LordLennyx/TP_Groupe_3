import { Request, Response } from "express";
import { Project, ProjectSchema } from "../models/project";
import { readDB, writeDB } from "../utils/fileManager";

// GET /projects
export const getAllProjects = (_: Request, res: Response) => {
  const projects = readDB();
  res.json(projects);
};

// POST /projects
export const createProject = (req: Request, res: Response) => {
  const result = ProjectSchema.safeParse(req.body);
  if (!result.success) return res.status(400).json(result.error);

  const projects = readDB();
  const newProject: Project = {
    ...result.data,
    id: projects.length ? projects[projects.length - 1].id! + 1 : 1,
    createdAt: new Date().toISOString(),
  };
  projects.push(newProject);
  writeDB(projects);
  return res.status(201).json(newProject);
};

// GET /projects/:id
export const getProjectById = (req: Request, res: Response) => {
  const id = Number(req.params.id);
  const projects = readDB();
  const project = projects.find((p) => p.id === id);
  if (!project) return res.status(404).json({ message: "Projet introuvable" });
  return res.json(project);
};

// PUT /projects/:id/grade
export const updateProjectGrade = (req: Request, res: Response) => {
  const id = Number(req.params.id);
  const { grade } = req.body as { grade: number };

  if (typeof grade !== "number" || grade < 0 || grade > 20) {
    return res.status(400).json({ message: "note invalide (0-20)" });
  }

  const projects = readDB();
  const index = projects.findIndex((p) => p.id === id);
  if (index === -1) return res.status(404).json({ message: "Projet introuvable" });

  projects[index].grade = grade;
  writeDB(projects);
  return res.json(projects[index]);
};

// DELETE /projects/:id
export const deleteProject = (req: Request, res: Response) => {
  const id = Number(req.params.id);
  const projects = readDB();
  const exists = projects.some((p) => p.id === id);
  if (!exists) return res.status(404).json({ message: "Projet introuvable" });

  const filtered = projects.filter((p) => p.id !== id);
  writeDB(filtered);
  return res.status(204).send();
};

// GET /projects/course/:courseName
export const getProjectsByCourse = (req: Request, res: Response) => {
  const { courseName } = req.params;
  const projects = readDB();
  const filtered = projects.filter(
    (p) => p.course.toLowerCase() === courseName.toLowerCase()
  );
  return res.json(filtered);
};
