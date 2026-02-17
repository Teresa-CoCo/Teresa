<div align="center">
  <img src="https://github.com/user-attachments/assets/2b24e837-e891-4c11-ab88-04de3ce44a24" align="centre" width="300" />
  <p><em>🤖 An AI-based tool made with Tauri + React 🤖</em></p>
</div>

---

## ✨ Features

- 💬 **AI Chat** - Chat with LLM models (OpenAI compatible API)
- 🧰 **Life Toolbox** - BMI calculator, ping tool, lucky numbers, unit converter, etc.
- 🎨 **Modern UI** - Beautiful interface with dark/light theme support
- 🌐 **Cross-platform** - Windows, macOS, Linux support

## 🚀 Quick Start

### Prerequisites

- [Node.js](https://nodejs.org/) 18+
- [Rust](https://rustup.rs/)
- [pnpm](https://pnpm.io/) (recommended) or npm/yarn

### Development

```bash
# Install dependencies
pnpm install

# Run in development mode
pnpm tauri dev
```

### Build

```bash
# Build for current platform
pnpm tauri build

# Or build for all platforms (requires cross-compilation setup)
```

## ⚙️ Configuration

Configure your AI API in the app settings:

| Setting | Description |
|---------|-------------|
| API URL | OpenAI compatible API endpoint |
| API Key | Your API key |
| Model | Model name (e.g., gpt-4, gpt-3.5-turbo) |

## 📦 Supported Platforms

- 🖥️ Windows (x64)
- 🍎 macOS (Intel & Apple Silicon)
- 🐧 Linux (AppImage, deb)

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript + TailwindCSS
- **Backend**: Tauri 2.0 (Rust)
- **Build**: Vite

## 📜 License

GPL-3.0

## 🙏 Thanks to

![VS Code](https://github.com/user-attachments/assets/67c65899-7e32-4cae-aa7c-0df9e39fa463)

![Tauri](https://github.com/user-attachments/assets/75425013-3642-4549-99e5-3400fbb5a66c)
