import { useState } from 'react';
import { Save, Check } from 'lucide-react';
import { AIConfig } from '../types';

interface SettingsProps {
  config: AIConfig;
  onSave: (config: AIConfig) => void;
}

export function Settings({ config, onSave }: SettingsProps) {
  const [apiUrl, setApiUrl] = useState(config.apiUrl);
  const [apiKey, setApiKey] = useState(config.apiKey);
  const [model, setModel] = useState(config.model);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    onSave({ apiUrl, apiKey, model });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">⚙️ 设置</h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">API 地址</label>
          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            placeholder="https://api.openai.com/v1"
            className="w-full rounded-lg border p-2 dark:bg-gray-800 dark:border-gray-600"
          />
          <p className="text-xs text-gray-500 mt-1">
            支持 OpenAI 兼容 API (如 OpenAI, Azure, Claude, 讯飞, 智谱等)
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">API Key</label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="sk-..."
            className="w-full rounded-lg border p-2 dark:bg-gray-800 dark:border-gray-600"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">模型名称</label>
          <input
            type="text"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            placeholder="gpt-3.5-turbo"
            className="w-full rounded-lg border p-2 dark:bg-gray-800 dark:border-gray-600"
          />
          <p className="text-xs text-gray-500 mt-1">
            常用: gpt-4, gpt-3.5-turbo, claude-3-opus, glm-4 等
          </p>
        </div>

        <button
          onClick={handleSave}
          className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
        >
          {saved ? <Check size={20} /> : <Save size={20} />}
          {saved ? '已保存' : '保存设置'}
        </button>
      </div>
    </div>
  );
}
