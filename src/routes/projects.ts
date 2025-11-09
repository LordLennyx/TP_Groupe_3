import * as express from "express";
import {
  createProject,
  getAllProjects,
  getProjectById,
  updateProjectGrade,
  deleteProject,
  getProjectsByCourse,
} from "../controllers/projectsController";

const router = express.Router();

router.get("/", getAllProjects);
router.post("/", createProject);
router.get("/:id", getProjectById);
router.put("/:id/grade", updateProjectGrade);
router.delete("/:id", deleteProject);
router.get("/course/:courseName", getProjectsByCourse);

export default router;
