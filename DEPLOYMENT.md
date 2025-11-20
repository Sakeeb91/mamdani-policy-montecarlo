# Deployment Guide

## Running the Streamlit Application Locally

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sakeeb91/mamdani-policy-montecarlo.git
   cd mamdani-policy-montecarlo
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: If you encounter issues with `pyarrow` (a Streamlit dependency), try:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install pyarrow --no-build-isolation
   pip install streamlit
   ```

   On macOS with Apple Silicon, you may need:
   ```bash
   brew install apache-arrow
   pip install pyarrow
   ```

4. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

5. **Access the application**:
   - The app will automatically open in your default browser
   - If not, navigate to: `http://localhost:8501`

### Command-Line Simulation

To run the Monte Carlo simulation without the web interface:

```bash
python main.py --simulations 10000 --threshold 2.0 --seed 42
```

## Deploying to Streamlit Cloud

### Step 1: Prepare Repository

Ensure your repository is pushed to GitHub with all files including:
- `app.py` (Streamlit application)
- `requirements.txt` (dependencies)
- `src/` directory (simulation code)

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Fill in:
   - **Repository**: `Sakeeb91/mamdani-policy-montecarlo`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy"

### Step 3: Configure (Optional)

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#262730"

[server]
maxUploadSize = 200
enableCORS = false
```

## Deploying to Other Platforms

### Heroku

1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port $PORT
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

3. Deploy:
   ```bash
   heroku create mamdani-policy-analysis
   git push heroku main
   ```

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t mamdani-analysis .
docker run -p 8501:8501 mamdani-analysis
```

### AWS EC2

1. Launch EC2 instance (Ubuntu 20.04+)
2. SSH into instance
3. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   ```
4. Clone repository and install:
   ```bash
   git clone https://github.com/Sakeeb91/mamdani-policy-montecarlo.git
   cd mamdani-policy-montecarlo
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Run with nohup:
   ```bash
   nohup streamlit run app.py --server.port 8501 &
   ```
6. Configure security group to allow port 8501

## Troubleshooting

### Common Issues

**Issue**: `pyarrow` installation fails
**Solution**:
```bash
# macOS
brew install apache-arrow

# Ubuntu/Debian
sudo apt-get install -y libarrow-dev

# Then install pyarrow
pip install pyarrow
```

**Issue**: Port 8501 already in use
**Solution**:
```bash
streamlit run app.py --server.port 8502
```

**Issue**: Module not found errors
**Solution**:
```bash
# Ensure you're in the project root directory
cd /path/to/mamdani-policy-montecarlo
# And virtual environment is activated
source venv/bin/activate
```

**Issue**: Simulations run slowly
**Solution**:
- Reduce number of simulations in sidebar (default: 5000)
- Use command-line version for large simulation runs
- Consider caching results with `@st.cache_data`

### Performance Optimization

For faster load times, add caching to `app.py`:

```python
import streamlit as st

@st.cache_data
def run_custom_simulation(...):
    # simulation code
    return results
```

## Environment Variables

You can set these via `.streamlit/secrets.toml` or environment variables:

```toml
# .streamlit/secrets.toml
[simulation]
default_simulations = 5000
default_threshold = 2.0
random_seed = 42
```

## Monitoring and Analytics

### Add Google Analytics

Create `.streamlit/config.toml`:

```toml
[browser]
gatherUsageStats = true
```

### Custom Analytics

Add to `app.py`:

```python
import streamlit as st

# Track page views
if 'page_views' not in st.session_state:
    st.session_state.page_views = 0
st.session_state.page_views += 1
```

## Security Considerations

1. **Input Validation**: All user inputs are validated and constrained
2. **No Data Storage**: Application doesn't store user data
3. **HTTPS**: Use HTTPS in production (automatic on Streamlit Cloud)
4. **Rate Limiting**: Consider adding rate limits for intensive simulations

## Updating the Application

To update a deployed app:

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: [description]"
   git push
   ```
3. Streamlit Cloud automatically redeploys on push

## Support

For issues or questions:
- **GitHub Issues**: [Create an issue](https://github.com/Sakeeb91/mamdani-policy-montecarlo/issues)
- **Email**: rahman.sakeeb@gmail.com
- **Documentation**: See [README.md](README.md) and [docs/](docs/)

---

**Last Updated**: November 20, 2025
