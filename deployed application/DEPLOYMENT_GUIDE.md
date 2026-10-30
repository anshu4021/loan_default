# 🌐 Production Deployment Guide

This guide covers deployment procedures for hosting the **Explainable AI for Loan Default Prediction** system across cloud platforms, container orchestrators, and free hosting tiers.

---

## 🚀 Option 1: Streamlit Community Cloud (Fastest & Free)

1. Push this repository to your GitHub account: `https://github.com/anshu4021/loan_default`.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **"New App"** and configure:
   - **Repository:** `anshu4021/loan_default`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy!"**
   - The app will build dependencies from `requirements.txt` and launch with a public URL: `https://loan-default-xai.streamlit.app/`.

---

## 🤗 Option 2: Hugging Face Spaces (Free Cloud Hosting)

1. Log into [huggingface.co](https://huggingface.co/) and click **New Space**.
2. Select **Streamlit** as the Space SDK and set hardware to **CPU Basic (Free)**.
3. Push or connect your GitHub repository `anshu4021/loan_default`.
4. Hugging Face will automatically detect `app.py` and deploy your interactive underwriting app with instant HTTPS.

---

## 🐳 Option 3: Docker Container Deployment

### Local Docker Build & Run:
```bash
# Build the container image
docker build -t loan-xai-app -f "deployed application/Dockerfile" .

# Run the container
docker run -d -p 8501:8501 --name loan-xai-container loan-xai-app
```
Access the application at `http://localhost:8501`.

### Docker Compose (Web App + REST API):
```bash
cd "deployed application"
docker-compose up -d
```
- Web Application: `http://localhost:8501`
- REST API Service: `http://localhost:8080/health`

---

## ☁️ Option 4: Render / Railway Cloud PaaS

1. Connect your repository `anshu4021/loan_default` on [Render.com](https://render.com/).
2. Select **Web Service** and choose **Python 3**.
3. Set the following build and start commands:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
4. Deploy the service.

---

## 🔒 Production Security & Hardening Checklist

- [x] **Non-Root User**: The Docker container runs under unprivileged UID `1000` (`appuser`).
- [x] **No Hardcoded Secrets**: Sensitive API keys and credentials are fed via environment variables.
- [x] **CORS & XSRF Protection**: Configured inside `.streamlit/config.toml` to guard against cross-origin attacks.
- [x] **Health Check Endpoint**: Automated probe at `/_stcore/health` for Kubernetes / ECS liveness probes.
- [x] **Bounded Memory Footprint**: Background explainer baselines are subsampled to maintain low RAM (<500 MB) during high-concurrency requests.
