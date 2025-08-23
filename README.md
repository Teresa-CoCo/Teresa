<div align="center">
  <img src="https://github.com/user-attachments/assets/2b24e837-e891-4c11-ab88-04de3ce44a24" align="centre" width="300" />
  <h1>Teresa V2 - AI Chat Assistant</h1>
  <p><em>🤖 A modern, feature-rich AI chat application built with Python and PyQt6 🤖</em></p>
</div>

---

## ✨ Features

### 🎨 Modern UI & User Experience
- [x] Beautiful dark/light themes with customizable accent colors
- [x] Modern chat bubble interface with smooth animations
- [x] Responsive layout with collapsible sidebar
- [x] Real-time typing indicators and streaming responses
- [x] System tray integration for background operation

### 🤖 AI Integration
- [x] Multiple AI provider support (DeepSeek, OpenAI, Claude)
- [x] Streaming response support for real-time conversation
- [x] Customizable AI parameters (temperature, max tokens, etc.)
- [x] Smart conversation context management
- [x] Error handling and retry mechanisms

### 💾 Advanced Data Management
- [x] SQLite database for efficient conversation storage
- [x] Conversation search and filtering
- [x] Favorite and archive conversation features
- [x] Automatic conversation titles generation
- [x] Statistics and analytics dashboard

### 📁 Export & Sharing
- [x] Export conversations in multiple formats (Markdown, HTML, TXT, JSON)
- [x] Conversation backup and restore
- [x] Smart conversation analysis and insights
- [x] Batch operations for conversation management

### ⚡ Productivity Features
- [x] Smart suggestions and auto-completion
- [x] Customizable keyboard shortcuts
- [x] Quick actions and command palette
- [x] Notification system for important events
- [x] Plugin architecture for extensibility

### 🔧 Customization
- [x] Comprehensive settings dialog
- [x] Font and appearance customization
- [x] Behavior and workflow preferences
- [x] API configuration management
- [x] Shortcut key customization

## 🛠️ How to Run

### Quick Start (Windows)
1. Download or clone this repository
2. Double-click `run.bat` to automatically set up and run Teresa V2
3. The script will create a virtual environment and install dependencies
4. Configure your API key in Settings (Ctrl+,) when the app opens

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/teresa-v2.git
cd teresa-v2

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python TeresaV2.py
```

### System Requirements
- Python 3.11 or later
- Windows 10/11, macOS, or Linux
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

## ⚗️ Configuration

### API Setup
1. Open Settings (Ctrl+, or File → Settings)
2. Go to the "API" tab
3. Select your preferred AI provider
4. Enter your API key
5. Adjust model parameters as needed

### Supported AI Providers
- **DeepSeek**: Cost-effective and powerful
- **OpenAI**: GPT-3.5/GPT-4 models
- **Claude**: Anthropic's Claude models
- **Local**: For local AI model integration

### Themes and Appearance
- Dark and Light themes
- Customizable accent colors
- Font family and size options
- Animation and effect controls
- Chat bubble style preferences

## 🏗️ Architecture

### Core Components
- **MainWindow**: Primary application interface
- **HistoryManager**: SQLite-based conversation management
- **AIProvider**: Multi-provider AI integration
- **ConfigManager**: Settings and preferences
- **FeatureManager**: Advanced functionality (search, export, etc.)

### Design Patterns
- Model-View-Controller (MVC) architecture
- Observer pattern for real-time updates
- Factory pattern for AI provider abstraction
- Plugin architecture for extensibility

## � Plugin Development

Teresa V2 supports plugins for extending functionality:

```python
from features import plugin_manager

class MyPlugin:
    def __init__(self):
        self.name = "My Plugin"
    
    def execute(self, context):
        # Plugin logic here
        pass

# Register plugin
plugin_manager.register_plugin("my_plugin", MyPlugin)
```

## 📊 Database Schema

### Conversations Table
- `id`: Unique conversation identifier
- `title`: Auto-generated conversation title
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `message_count`: Number of messages
- `total_tokens`: Estimated token usage
- `is_favorite`: Favorite status
- `is_archived`: Archive status

### Messages Table
- `id`: Message identifier
- `conversation_id`: Foreign key to conversations
- `role`: Message role (user/assistant/system)
- `content`: Message content
- `timestamp`: Message timestamp
- `token_count`: Estimated tokens

## 🚀 Performance Optimizations

- Lazy loading for large conversation lists
- SQLite indexing for fast searches
- Asynchronous AI API calls
- Memory-efficient message rendering
- Background auto-save operations

## 🔒 Privacy & Security

- Local data storage only
- API keys encrypted in configuration
- No telemetry or usage tracking
- Optional conversation encryption
- Secure API communication

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
python -m black .
python -m isort .
```

## 📝 Changelog

### Version 2.0.0 (Latest)
- Complete UI redesign with modern components
- SQLite database integration
- Multi-provider AI support
- Advanced conversation management
- Export functionality
- Plugin system
- Comprehensive settings

### Version 1.0.0
- Basic chat functionality
- Simple history management
- DeepSeek integration

## 📜 License

This project is licensed under the GPL v3 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyQt6**: Powerful GUI framework
- **OpenAI**: API integration libraries
- **SQLite**: Reliable database engine
- **Contributors**: Everyone who helped improve Teresa V2

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/teresa-v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/teresa-v2/discussions)
- **Email**: support@teresa-ai.com

---

<div align="center">
  <p>Made with ❤️ by the Teresa Development Team</p>
  <p>⭐ Star this repository if you find it useful!</p>
</div>
