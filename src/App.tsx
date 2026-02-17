import { useState, useEffect } from 'react';
import { MessageCircle, Settings, Wrench, Monitor } from 'lucide-react';
import { Chat } from './components/Chat';
import { Settings as SettingsPanel } from './components/Settings';
import { LifeTool } from './components/LifeTool';
import { AIConfig } from './types';
import { getConfig, saveConfig } from './utils/configStore';

type Tab = 'chat' | 'tools' | 'settings';

function App() {
  const [config, setConfig] = useState<AIConfig>(getConfig());
  const [activeTab, setActiveTab] = useState<Tab>('chat');

  useEffect(() => {
    const saved = getConfig();
    setConfig(saved);
  }, []);

  const handleSaveConfig = (newConfig: AIConfig) => {
    saveConfig(newConfig);
    setConfig(newConfig);
  };

  const tabs = [
    { id: 'chat' as Tab, name: '聊天', icon: MessageCircle },
    { id: 'tools' as Tab, name: '工具箱', icon: Wrench },
    { id: 'settings' as Tab, name: '设置', icon: Settings },
  ];

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-3 border-b">
        <div className="flex items-center gap-2">
          <Monitor className="w-6 h-6" />
          <h1 className="text-xl font-bold">Teresa AI</h1>
        </div>
        
        {/* Status indicator */}
        <div className="flex items-center gap-2 text-sm">
          {config.apiKey ? (
            <span className="flex items-center gap-1 text-green-500">
              <span className="w-2 h-2 bg-green-500 rounded-full"></span>
              已连接
            </span>
          ) : (
            <span className="flex items-center gap-1 text-yellow-500">
              <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
              未配置
            </span>
          )}
        </div>
      </header>

      {/* Tab Navigation */}
      <nav className="flex border-b">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 transition-colors ${
                activeTab === tab.id
                  ? 'border-b-2 border-blue-500 text-blue-500'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <Icon size={18} />
              {tab.name}
            </button>
          );
        })}
      </nav>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        {activeTab === 'chat' && <Chat config={config} />}
        {activeTab === 'tools' && <LifeTool />}
        {activeTab === 'settings' && (
          <SettingsPanel config={config} onSave={handleSaveConfig} />
        )}
      </main>
    </div>
  );
}

export default App;
