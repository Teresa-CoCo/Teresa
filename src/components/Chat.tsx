import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Camera, X, ImageIcon, Upload } from 'lucide-react';
import { ChatMessage, AIConfig, MessageContentPart } from '../types';
import { streamChat } from '../utils/api';
import { invoke } from '@tauri-apps/api/core';

interface ChatProps {
  config: AIConfig;
}

/** 从 ChatMessage.content 中提取纯文本，用于 UI 显示 */
function extractText(content: ChatMessage['content']): string {
  if (typeof content === 'string') return content;
  return content
    .filter((p): p is { type: 'text'; text: string } => p.type === 'text')
    .map((p) => p.text)
    .join('');
}

/** 从 ChatMessage.content 中提取图片 URL 列表 */
function extractImages(content: ChatMessage['content']): string[] {
  if (typeof content === 'string') return [];
  return content
    .filter(
      (p): p is { type: 'image_url'; image_url: { url: string } } =>
        p.type === 'image_url'
    )
    .map((p) => p.image_url.url);
}

export function Chat({ config }: ChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // 待发送的图片（base64 data URI）
  const [pendingImages, setPendingImages] = useState<string[]>([]);
  const [screenshotLoading, setScreenshotLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  /** 截取全屏 */
  const handleScreenshot = async () => {
    if (!config.visionEnabled) return;
    setScreenshotLoading(true);
    try {
      const dataUri = await invoke<string>('capture_screenshot');
      setPendingImages((prev) => [...prev, dataUri]);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setScreenshotLoading(false);
    }
  };

  /** 从文件上传图片 */
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files ?? []);
    files.forEach((file) => {
      const reader = new FileReader();
      reader.onload = () => {
        if (typeof reader.result === 'string') {
          setPendingImages((prev) => [...prev, reader.result as string]);
        }
      };
      reader.readAsDataURL(file);
    });
    // 重置 input，允许重复上传同一文件
    e.target.value = '';
  };

  const removePendingImage = (index: number) => {
    setPendingImages((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSend = async () => {
    const hasText = input.trim().length > 0;
    const hasImages = pendingImages.length > 0;
    if ((!hasText && !hasImages) || !config.apiKey) return;

    // 构建消息内容
    let messageContent: ChatMessage['content'];
    if (hasImages) {
      const parts: MessageContentPart[] = [];
      if (hasText) parts.push({ type: 'text', text: input.trim() });
      pendingImages.forEach((url) =>
        parts.push({ type: 'image_url', image_url: { url, detail: 'auto' } })
      );
      messageContent = parts;
    } else {
      messageContent = input.trim();
    }

    const userMessage: ChatMessage = { role: 'user', content: messageContent };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setPendingImages([]);
    setLoading(true);
    setError(null);

    try {
      const allMessages: ChatMessage[] = [...messages, userMessage];
      let assistantContent = '';

      for await (const chunk of streamChat(config, allMessages)) {
        assistantContent += chunk;
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last && last.role === 'assistant') {
            return [...prev.slice(0, -1), { ...last, content: assistantContent }];
          }
          return [...prev, { role: 'assistant', content: assistantContent }];
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const canSend =
    config.apiKey && !loading && (input.trim().length > 0 || pendingImages.length > 0);

  return (
    <div className="flex flex-col h-full">
      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg">👋 你好！我是 Teresa AI</p>
            <p className="mt-2">请在设置中配置你的 API，然后开始聊天吧</p>
            {config.visionEnabled && (
              <p className="mt-1 text-sm text-blue-500">📷 视觉功能已启用，可截图发送给 AI</p>
            )}
          </div>
        )}

        {messages.map((msg, idx) => {
          const text = extractText(msg.content);
          const images = extractImages(msg.content);
          return (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 space-y-2 ${
                  msg.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 dark:bg-gray-700'
                }`}
              >
                {images.map((src, i) => (
                  <img
                    key={i}
                    src={src}
                    alt="附图"
                    className="max-w-full rounded max-h-48 object-contain"
                  />
                ))}
                {text && <p className="whitespace-pre-wrap">{text}</p>}
              </div>
            </div>
          );
        })}

        {error && (
          <div className="text-red-500 text-center p-2 bg-red-100 rounded">
            {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* 待发送图片预览 */}
      {pendingImages.length > 0 && (
        <div className="flex gap-2 px-4 py-2 border-t flex-wrap">
          {pendingImages.map((src, i) => (
            <div key={i} className="relative">
              <img
                src={src}
                alt="待发送"
                className="h-16 w-16 object-cover rounded border"
              />
              <button
                onClick={() => removePendingImage(i)}
                className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center text-xs"
              >
                <X size={10} />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* 输入区 */}
      <div className="border-t p-4">
        <div className="flex gap-2 items-end">
          {/* 截图 & 上传按钮（仅视觉模式开启时显示） */}
          {config.visionEnabled && (
            <div className="flex gap-1">
              <button
                onClick={handleScreenshot}
                disabled={screenshotLoading || loading}
                title="截取屏幕"
                className="p-2 rounded-lg border hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50"
              >
                {screenshotLoading ? (
                  <Loader2 size={18} className="animate-spin" />
                ) : (
                  <Camera size={18} />
                )}
              </button>
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={loading}
                title="上传图片"
                className="p-2 rounded-lg border hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50"
              >
                <Upload size={18} />
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                multiple
                className="hidden"
                onChange={handleFileUpload}
              />
            </div>
          )}

          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              config.apiKey
                ? config.visionEnabled
                  ? '输入消息，或截图发给 AI...'
                  : '输入消息...'
                : '请先在设置中配置 API Key'
            }
            disabled={!config.apiKey || loading}
            className="flex-1 resize-none rounded-lg border p-2 dark:bg-gray-800 dark:border-gray-600"
            rows={2}
          />
          <button
            onClick={handleSend}
            disabled={!canSend}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 self-end"
          >
            {loading ? <Loader2 className="animate-spin" /> : <Send size={20} />}
          </button>
        </div>

        {/* 视觉功能未开启时的提示 */}
        {!config.visionEnabled && (
          <p className="text-xs text-gray-400 mt-1 flex items-center gap-1">
            <ImageIcon size={12} />
            在设置中开启「视觉功能」可截图发送给 AI
          </p>
        )}
      </div>
    </div>
  );
}
