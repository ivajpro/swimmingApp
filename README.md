# 🏊 Swimming Training Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Beta-orange.svg)

A modern, user-friendly desktop application to track your swimming training sessions with style.

<p align="center">
  <img src="docs/images/app_preview.png" alt="App Preview" width="800">
</p>

## ✨ Features

- 🎯 **Session Tracking**
  - Record swimming sessions with detailed metrics
  - Track multiple sets per session
  - Support for all swimming styles including mixed styles
  - Rest interval tracking

- 📊 **Statistics & Analysis**
  - Visualize your progress over time
  - Track total distance, time, and sets
  - Analyze performance trends

- 🎨 **Modern UI**
  - Clean, intuitive interface
  - Dark/Light theme support
  - Smooth animations and transitions
  - Responsive design

- 💾 **Data Management**
  - Local JSON storage
  - CSV export functionality
  - Session backup support

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

The project requires the following main packages:
- `customtkinter`: Modern UI components
- `tkinter`: GUI framework (included with Python)
- `sqlite3`: Database management (included with Python)

To install all dependencies:
```powershell
pip install -r requirements.txt
```

Note: Some dependencies are part of Python's standard library and don't need separate installation.

## 🛠️ Tech Stack

- **Frontend**: CustomTkinter
- **Storage**: JSON/CSV
- **Language**: Python 3.10+
- **Testing**: pytest

### Running Tests
```bash
python -m pytest tests/
```

## Project Structure
```
swimmingApp/
├── src/           # Source code
├── tests/         # Test files
├── data/          # Data storage
└── docs/          # Documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Upcoming Features

- [ ] Cloud synchronization
- [ ] Training templates
- [ ] Mobile companion app
- [ ] Advanced statistics
- [ ] Multi-language support

## 🙏 Acknowledgments

- CustomTkinter for the modern UI components
- All contributors and testers

---
<p align="center">
  Made with ❤️ for swimmers
</p>
