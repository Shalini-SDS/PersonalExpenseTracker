# Personal Expense Tracker - Requirements

## Required Dependencies
None! The project uses only Python Standard Library.

## Optional Dependencies (For Enhanced Features)

### For Visualization/Charts Feature
```
matplotlib>=3.3.0
```

### Install Optional Dependencies
```bash
# Using pip
pip install -r requirements_optional.txt

# Or manually
pip install matplotlib
```

## Tested Python Versions
- Python 3.6
- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

## System Requirements
- **RAM**: Minimum 256MB (no practical limit for typical usage)
- **Disk Space**: 1MB for application + data file storage
- **OS**: Windows, macOS, Linux
- **Internet**: Not required (100% offline operation)

## Installation Instructions

### Windows
```powershell
# Ensure Python is installed
python --version

# Optional: Install matplotlib
pip install matplotlib
```

### macOS
```bash
# Using system Python 3
python3 --version

# Optional: Install matplotlib
pip3 install matplotlib
```

### Linux (Ubuntu/Debian)
```bash
# Install Python 3 and pip
sudo apt-get install python3 python3-pip

# Optional: Install matplotlib
pip3 install matplotlib
```

### Docker (Optional)
If you want to run in a container:

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY expense_tracker.py .

# Optional: Install matplotlib
RUN pip install matplotlib

CMD ["python", "expense_tracker.py"]
```

Build and run:
```bash
docker build -t expense-tracker .
docker run -it -v $(pwd):/app expense-tracker
```

## Verification

### Verify Installation
```bash
# Check Python
python --version  # Should be 3.6+

# Check installed packages
pip list

# Run program
python expense_tracker.py
```

### Test Optional Features
```bash
# Test matplotlib import
python -c "import matplotlib; print('matplotlib OK')"

# If error, install:
pip install matplotlib
```

## Troubleshooting Dependencies

### pip not found
```bash
# Windows
python -m pip --version

# macOS/Linux
python3 -m pip --version
```

### Permission denied (macOS/Linux)
```bash
# Use user install
pip install --user matplotlib
```

### matplotlib installation issues
```bash
# Try upgrade pip first
pip install --upgrade pip

# Then install matplotlib
pip install matplotlib
```

## Virtual Environment (Recommended)

### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies in Virtual Environment
```bash
pip install -r requirements_optional.txt
```

### Deactivate Virtual Environment
```bash
# Windows
deactivate

# macOS/Linux
deactivate
```

## Conda Users

```bash
# Create environment
conda create -n expense-tracker python=3.11

# Activate environment
conda activate expense-tracker

# Install optional packages
conda install matplotlib

# Run program
python expense_tracker.py
```

## Project Dependencies Explained

### Standard Library (Built-in)
- **json**: Data serialization (built-in)
- **os**: File operations (built-in)
- **datetime**: Date/time handling (built-in)
- **collections**: Data structures (built-in)

These are ALWAYS available with Python and don't need installation.

### Optional Packages
- **matplotlib**: Visualization/charting (optional)
  - Required for: Feature #5 (Visualize Expenses)
  - Can be skipped if you don't need charts
  - Installation: `pip install matplotlib`

- **pytesseract** + **Pillow**: OCR support for receipt uploads
  - Required for: Receipt OCR (Upload and auto-extract amount/date/description)
  - Installation: `pip install pytesseract Pillow`
  - Note: The Tesseract OCR engine must be installed on your system separately:
    - Windows: Download from https://github.com/tesseract-ocr/tesseract and add to PATH
    - macOS: `brew install tesseract`
    - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`

- **python-dateutil**: Flexible date parsing used to extract dates from receipts
  - Installation: `pip install python-dateutil`

## Version Compatibility

### matplotlib Versions
- matplotlib 3.3.0 - 3.8.x: All compatible
- Older versions may lack some features
- Newer versions recommended for best performance

### Python Version Impact
| Version | Status | Notes |
|---------|--------|-------|
| 3.6 | ✅ Supported | Oldest supported version |
| 3.7 | ✅ Supported | Stable |
| 3.8 | ✅ Supported | Stable |
| 3.9 | ✅ Supported | Stable |
| 3.10 | ✅ Supported | Stable |
| 3.11 | ✅ Supported | Latest stable |
| 3.12 | ✅ Supported | Latest stable |
| 2.7 | ❌ Not supported | Python 2 is deprecated |

## Offline Installation

If you don't have internet access:

1. On a connected computer, download packages:
   ```bash
   pip download matplotlib -d ./packages
   ```

2. Transfer the `packages` folder to offline computer

3. Install from local packages:
   ```bash
   pip install --no-index --find-links ./packages matplotlib
   ```

## Continuous Integration / Deployment

### GitHub Actions Example
```yaml
name: Test

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install matplotlib
      - name: Run program
        run: python expense_tracker.py
```

## Support for Multiple Python Installations

If you have multiple Python versions:

```bash
# Windows
py -3.11 expense_tracker.py  # Use Python 3.11
py -3.10 expense_tracker.py  # Use Python 3.10

# macOS/Linux
python3.11 expense_tracker.py
python3.10 expense_tracker.py
```

## FreezePy / Executable Creation

To create standalone executables:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile expense_tracker.py

# Executable in dist/ folder
```

## Uninstall

```bash
# Remove program
rm -r PersonalExpenseTracker-1/

# Remove optional dependencies
pip uninstall matplotlib

# Clean pip cache
pip cache purge
```

## Getting Help

- **Python not installed?** → Download from python.org
- **pip issues?** → Try: `python -m pip install --upgrade pip`
- **matplotlib errors?** → Check: `pip install --upgrade matplotlib`
- **Other issues?** → Check Python version compatibility above

---

## Quick Reference Commands

```bash
# Check Python version
python --version

# Install optional features
pip install matplotlib

# List installed packages
pip list

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Run program
python expense_tracker.py

# Deactivate virtual environment
deactivate
```

---

**Last Updated**: November 26, 2024
**Maintained By**: Development Team

For latest updates, check: python.org and matplotlib.org
