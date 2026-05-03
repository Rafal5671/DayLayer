export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Note {
  id: number;
  title: string;
  content: string;
  tags: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  priority: "low" | "medium" | "high";
  status: "todo" | "in_progress" | "done";
  deadline: string | null;
  created_at: string;
  updated_at: string;
}

export interface Bookmark {
  id: number;
  url: string;
  title: string;
  description: string;
  thumbnail: string;
  tags: string;
  is_scraped: boolean;
  created_at: string;
  updated_at: string;
}
