// Configuration types
export interface AIConfig {
  apiUrl: string;
  apiKey: string;
  model: string;
  visionEnabled?: boolean; // 是否启用视觉功能
}

// 多模态消息内容（文本 + 图片）
export type MessageContentPart =
  | { type: 'text'; text: string }
  | { type: 'image_url'; image_url: { url: string; detail?: 'auto' | 'low' | 'high' } };

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string | MessageContentPart[];
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
