# BIM Portal Python Client - Hackathon Edition

Quick access to the German BIM Portal API for hackathons and rapid prototyping.

## Setup

This project requires Python 3.12 or higher. All exports will be saved to the `exports/` directory.

### Recommended: `venv` and `pip`

This is the standard, lightweight way to set up a Python project.

**Linux/macOS:**
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Windows:**
```powershell
# Create a virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Alternative: `conda`

If you prefer using Conda, you can use the provided `environment.yml` file.

**Linux/macOS/Windows:**
```bash
# Create the environment from the file
conda env create -f environment.yml

# Activate the environment
conda activate bim-portal-hackathon
```

## 🚀 Quick Start
### 0. Create and account in the BIM Portal website (EDU environment)
Visit: https://via.bund.de/bmdv/bim-portal/edu/bim and click on register.

### 1. Configure Credentials
```bash
cp env.example .env
# Edit .env with your BIM Portal credentials used for registration:
# BIM_PORTAL_USERNAME="your-email@example.com"
# BIM_PORTAL_PASSWORD="your-password"
```

### 2. Run Example

**Method 1: IDE (Recommended for Development)**
- Open `hackathon_example/hackathon_example.py` in your IDE
- Click the "Run" (or debug) button

**Method 2: Command Line (Recommended for Consistency)**
```bash
python -m hackathon_example.hackathon_example
```

## 💡 Hackathon Code Template

Edit `hackathon_example/hackathon_example.py` and add your code to the `run_hackathon_code()` function:

```python
def run_hackathon_code(client):
    # Your hackathon code here!
    projects = client.search_projects()
    loins = client.search_loins()
    properties = client.search_properties()
    
    # Export examples
    if projects:
        pdf_content = client.export_project_pdf(projects[0].guid)
        # Save using ExportUtils.save_export_file()
```

## 📚 Key Methods

```python
# Search
projects = client.search_projects()
loins = client.search_loins() 
properties = client.search_properties()

# Get Details
project = client.get_project(guid)
loin = client.get_loin(guid)

# Export (returns bytes)
pdf = client.export_project_pdf(guid)
ids = client.export_loin_ids(guid)
xml = client.export_loin_xml(guid)
```

## 🔧 Health Check
```bash
python examples/health_check.py
```

## 📂 File Structure
- `hackathon_example/` - **Start here!** Your main workspace
- `examples/` - Advanced examples and utilities
- `client/` - Core API client (don't modify)
- `exports/` - Downloaded files saved here

## 🎯 Tips for Hackathon Success

1. **Start with the template**: Run `from hackathon_example import main` first
2. **Use the examples**: Copy patterns from `examples/export_examples/`
3. **Save files properly**: Use `ExportUtils.save_export_file()` for exports
4. **Test connection**: Run health check if you have issues

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | Run `pip install -e .` |
| Auth failed | Check `.env` file exists and has correct credentials |
| No data found | Try broader search terms or check permissions |
| Connection issues | Run `python examples/health_check.py` |

**Need BIM Portal access?** Visit: https://via.bund.de/bmdv/bim-portal/edu/bim

---
**Ready to hack!** 🚀 Edit `hackathon_example/hackathon_example.py` and start building!