# 🏊 Swimming Training Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Beta-orange.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-success.svg)

A modern, user-friendly desktop application to track your swimming training sessions.

<p align="center">
  <img src="docs/images/app_preview.png" alt="App Preview" width="800">
</p>

## ✨ Current Features (v1.0.0)

- 🎯 **Session Tracking**
  - Record swimming sessions with basic metrics
  - Track duration and distance
  - Support for different stroke types
  - Session notes functionality

- 🎨 **Modern UI**
  - Clean, intuitive dark mode interface
  - Blue theme accents
  - CustomTkinter components

- 💾 **Data Management**
  - SQLite database storage
  - Persistent data between sessions
  - Secure data handling

## Documentation
- [User Guide](docs/USER_GUIDE.md) - Getting started and basic usage
- [Features Guide](docs/FEATURES.md) - Detailed feature documentation

## 🚀 Quick Start

1. **Prerequisites**
   ```powershell
   # Check Python version (3.10+ required)
   python --version
   ```

2. **Installation**
   ```powershell
# Clone the repository
   git clone https://github.com/yourusername/swimmingApp.git
   cd swimmingApp

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```powershell
   python -m src.main
   ```

## 📦 Dependencies

Core requirements:
- `customtkinter>=5.2.0`: Modern UI components
- `tkinter`: GUI framework (included with Python)
- `sqlite3`: Database management (included with Python)

To install required dependencies:
```powershell
pip install -r requirements.txt
```

## 🛠️ Project Structure
```
swimmingApp/
├── src/
│   ├── main.py              # Application entry point
│   ├── gui/
│   │   └── main_window.py   # Main window interface
│   └── data/
│       ├── database.py      # Database operations
│       └── swimming.db      # SQLite database
└── README.md
```

## 🎯 Roadmap

- [ ] Session statistics and analytics
- [ ] Data export functionality
- [ ] Training plan templates
- [ ] Performance graphs
- [ ] Backup/restore capability

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
<p align="center">
  Made with 💙 for swimmers
</p>
