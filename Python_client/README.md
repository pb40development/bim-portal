# BIM Portal Python Client - Hackathon Edition

Quick access to the German BIM Portal API for hackathons and rapid prototyping.

## 🚀 Quick Installation

**Recommended approach:**
```bash
# Clone and install in development mode
git clone https://github.com/pb40development/bim-portal
cd bim-portal/Python_client
```

This project requires Python 3.12 or higher. All exports will be saved to the exports/ directory.

<details>
<summary>🐍 <strong>Virtual Environment Setup (Recommended)</strong></summary>

### Using `venv` (Standard Python)

**Linux/macOS:**
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install the package in development mode
pip install -e .
```

**Windows:**
```powershell
# Create a virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# Install the package in development mode
pip install -e .
```

### Using `pip` with requirements.txt insteaad of `pip install -e .`
```bash
# Alternative: Install from requirements file
pip install -r requirements.txt
```

**Why `pip install -e .` is better:**
- ✅ **Edit and test immediately**: Changes to your code work instantly without reinstalling.
- ✅ **Proper package structure**: Your code becomes a proper Python package you can import anywhere.
- ✅ **No path issues**: Import `from hackathon_example import main` works from any directory.
- ❌ **requirements.txt**: Only installs dependencies, you might get import errors for your own code if you are not doing proper imports.

</details>

<details>
<summary>🐍 <strong>Alternative: Conda Environment</strong></summary>

If you prefer using Conda, you can use the provided `environment.yml` file.

**Linux/macOS/Windows:**
```bash
# Create the environment from the file
conda env create -f environment.yml

# Activate the environment
conda activate bim-portal-hackathon

# Install the package in development mode
pip install -e .
```
</details>




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

## Run Examples

**Method 1: IDE (Recommended for Development)**
- Open `\examples\export_examples\loin_export_example.py` in your IDE
- Click the "Run" (or Debug) button

**Method 2: Command Line (from Python_client directory)**
```bash
 python .\examples\export_examples\loin_export_example.py
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