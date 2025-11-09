import * as fs from "fs";
import * as path from "path";
import { Project } from "../models/project";

const dbPath = path.join(__dirname, "../../db.json");

export const readDB = (): Project[] => {
  if (!fs.existsSync(dbPath)) fs.writeFileSync(dbPath, "[]", "utf-8");
  const data = fs.readFileSync(dbPath, "utf-8");
  return JSON.parse(data);
};

export const writeDB = (projects: Project[]): void => {
  fs.writeFileSync(dbPath, JSON.stringify(projects, null, 2));
};