import axios from "axios";
axios.defaults.baseURL = "http://localhost:3001";

export interface ChartData {
  positive: number;
  negative: number;
  neutral: number;
}

export interface CommentCommand {
  command: string;
  mood: Mood;
}

export async function getCommentCommandAndMood(comment: string) {
  const { data } = await axios.get<CommentCommand>("/", {
    params: {
      comment,
    },
  });
  return data;
}

export interface Command {
  command: string;
  positive: number;
  negative: number;
}

export async function getCommands() {
  const { data } = await axios.get<Command[]>("/");
  return data;
}

export enum Mood {
  Positive,
  Negative,
}

export interface Comment {
  text: string;
  mood: Mood;
}

export async function getCommandComments(command: string) {
  const { data } = await axios.get<Comment[]>("/", {
    params: {
      command,
    },
  });
  return data;
}
