import { AIConfig } from '../types';

// Default configuration
const defaultConfig: AIConfig = {
  apiUrl: 'https://api.openai.com/v1',
  apiKey: '',
  model: 'gpt-3.5-turbo',
};

// Get config from localStorage
export function getConfig(): AIConfig {
  try {
    const stored = localStorage.getItem('teresa-config');
    if (stored) {
      return { ...defaultConfig, ...JSON.parse(stored) };
    }
  } catch (e) {
    console.error('Failed to load config:', e);
  }
  return defaultConfig;
}

// Save config to localStorage
export function saveConfig(config: AIConfig): void {
  try {
    localStorage.setItem('teresa-config', JSON.stringify(config));
  } catch (e) {
    console.error('Failed to save config:', e);
  }
}

// Export default config for reference
export { defaultConfig };
