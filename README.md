<div align="center">
  <img src="https://raw.githubusercontent.com/teresa-ai/teresa/main/logo.ico" align="centre" width="128" />
  <h1>Teresa AI</h1>
  <p><em>🤖 An AI-based tool made with Tauri + React 🤖</em></p>
</div>

---
<p align="center">
  <a href="https://github.com/teresa-ai/teresa/releases">
    <img src="https://img.shields.io/github/v/release/teresa-ai/teresa?include_prereleases&style=flat-square" alt="Release" />
  </a>
  <a href="https://github.com/teresa-ai/teresa/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/teresa-ai/teresa?style=flat-square" alt="License" />
  </a>
  <a href="https://github.com/teresa-ai/teresa/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/teresa-ai/teresa/release.yml?style=flat-square" alt="Build" />
  </a>
</p>

---

## ✨ Features

- [x] **AI Chat** - Chat with LLM using OpenAI-compatible APIs
- [x] **ToolBox** - Life tools including BMI calculator, electrical calculator, lucky number generator, length converter, binary/decimal converter
- [x] **Cross-Platform** - Supports Windows, macOS, and Linux
- [x] **Custom API** - Configure any OpenAI-compatible API (OpenAI, Azure, Claude, GLM, Spark, etc.)
- [x] **Modern UI** - Beautiful interface with dark/light mode support

## 🛠️ How to Run

### Pre-built Binaries

Download the latest release from the [Releases](https://github.com/teresa-ai/teresa/releases) page:

- **Windows**: Download `.exe` or `.msi` installer
- **macOS**: Download `.dmg` installer
- **Linux**: Download `.AppImage` or `.deb` package

### From Source

#### Prerequisites

- [Node.js](https://nodejs.org/) 18+
- [Rust](https://rustup.rs/) 1.70+
- [npm](https://www.npmjs.com/)

#### Installation

```bash
# Clone the repository
git clone https://github.com/teresa-ai/teresa.git
cd teresa

# Install dependencies
npm install

# Run in development mode
npm run tauri dev
```

#### Build

```bash
# Build for your current platform
npm run tauri build

# Build for all platforms
npm run tauri build -- --target x86_64-pc-windows-msvc  # Windows
npm run tauri build -- --target aarch64-apple-darwin     # macOS ARM
npm run tauri build -- --target x86_64-unknown-linux-gnu # Linux
```

## ⚙️ Configuration

### AI API Setup

On first launch, go to the **Settings** tab to configure your AI API:

1. **API URL**: Enter your OpenAI-compatible API endpoint
   - OpenAI: `https://api.openai.com/v1`
   - Azure: `https://your-resource.openai.azure.com/openai/deployments/your-deployment`
   - Claude: `https://api.anthropic.com/v1`
   - GLM: `https://open.bigmodel.cn/api/paas/v4`
   - Spark: `https://spark-api.xf-yun.com/v3.5`

2. **API Key**: Enter your API key

3. **Model**: Enter the model name
   - OpenAI: `gpt-4`, `gpt-3.5-turbo`
   - Claude: `claude-3-opus`, `claude-3-sonnet`
   - GLM: `glm-4`, `glm-3-turbo`
   - Spark: `spark-3.5`

### Supported APIs

Teresa is compatible with any OpenAI-compatible API, including:

| Provider | API URL Example |
|----------|-----------------|
| OpenAI | `https://api.openai.com/v1` |
| Azure OpenAI | `https://your-resource.openai.azure.com/openai/deployments/your-deployment` |
| Anthropic Claude | `https://api.anthropic.com/v1` |
| 智谱 GLM | `https://open.bigmodel.cn/api/paas/v4` |
| 讯飞星火 | `https://spark-api.xf-yun.com/v3.5` |
| 百度文心 | `https://qianfan.baidubce.com/v2` |
| 阿里通义 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

## 📁 Project Structure

```
teresa/
├── src/                    # Frontend source code
│   ├── components/        # React components
│   │   ├── Chat.tsx       # AI chat component
│   │   ├── Settings.tsx  # Settings panel
│   │   └── LifeTool.tsx  # Life tools
│   ├── utils/            # Utility functions
│   │   ├── api.ts        # API client
│   │   ├── configStore.ts # Configuration storage
│   │   └── tools.ts      # Tool functions
│   ├── types.ts          # TypeScript types
│   ├── App.tsx           # Main application
│   └── main.tsx          # Entry point
├── src-tauri/            # Tauri backend (Rust)
│   ├── src/             # Rust source code
│   │   ├── lib.rs       # Library functions
│   │   └── main.rs     # Entry point
│   ├── Cargo.toml       # Rust dependencies
│   ├── tauri.conf.json  # Tauri configuration
│   └── capabilities/   # Permission capabilities
├── package.json          # Node.js dependencies
├── vite.config.ts       # Vite configuration
├── tailwind.config.js   # TailwindCSS configuration
└── logo.ico             # Application icon
```

## 🔧 Tech Stack

- **Frontend**: React 18 + TypeScript + TailwindCSS
- **Backend**: Tauri 2.0 (Rust)
- **Build**: Vite
- **Icons**: Lucide React

## 📜 License

This project is licensed under the [GPL-3.0 License](LICENSE).

## 🙏 Thanks To

<p align="center">
  <a href="https://code.visualstudio.com/">
    <img src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg" width="64" alt="VS Code" />
  </a>
  <a href="https://tauri.app/">
    <img src="https://tauri.app/favicon.ico" width="64" alt="Tauri" />
  </a>
  <a href="https://react.dev/">
    <img src="https://react.dev/favicon.ico" width="64" alt="React" />
  </a>
</p>
