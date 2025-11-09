import { z } from "zod";

export const ProjectSchema = z.object({
  id: z.number().optional(),
  title: z.string().min(3),
  description: z.string().optional(),
  course: z.string(),
  grade: z.number().min(0).max(20).optional(),
  createdAt: z.string().optional(),
});

export type Project = z.infer<typeof ProjectSchema>;