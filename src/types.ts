// Configuration types
export interface AIConfig {
  apiUrl: string;
  apiKey: string;
  model: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatRequest {
  model: string;
  messages: ChatMessage[];
  stream?: boolean;
}

export interface ChatResponse {
  id: string;
  choices: {
    message: ChatMessage;
    finish_reason: string;
  }[];
}

export interface ChatChunk {
  choices: {
    delta: Partial<ChatMessage>;
    finish_reason?: string;
  }[];
}
