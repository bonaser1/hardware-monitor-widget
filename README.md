# Windows Desktop Performance Monitor Widget

A lightweight, frameless desktop widget written in Python that displays real-time CPU, RAM, and GPU usage. The widget is pinned directly to the Windows desktop background, and does not steal focus or cause terminal window flickering.

## Features

- **Real-Time Tracking:** Updates CPU, RAM, and GPU usage metrics every second.
- **Desktop Integration:** Anchored to the desktop Z-order (stays behind open applications).
- **No Window Flickering:** Uses native WMI performance counters instead of CLI subprocess spawning to fetch GPU stats.
- **Click-Through/No Activation:** Does not grab keyboard or mouse focus when clicked.

## Prerequisites

- Windows 10 or 11
- Python 3.8 or higher

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bonaser1/hardware-monitor-widget.git
   cd hardware-monitor-widget

Or simply place the files in any folder:

```
hardware-monitor-widget/
├── desktop_widget.py
├── requirements.txt
└── README.md
```

### 2 — Create a virtual environment (recommended)

```cmd
python -m venv .venv
.venv\Scripts\Activate.bat
```

### 3 — Install dependencies

```cmd
pip install -r requirements.txt
```

---

## Running the Widget

```cmd
python main.py
```

The widget appears immediately in the bottom-right corner of your screen above the taskbar notification area.

### Start automatically with Windows

1. Press `Win + R`, type `shell:startup`, press Enter.
2. Create a shortcut in that folder pointing to:

   ```
   pythonw.exe "C:\full\path\to\hardware-monitor-widget\desktop_widget.py"
   ```

   Using `pythonw.exe` (note the **w**) suppresses the console window.

---
