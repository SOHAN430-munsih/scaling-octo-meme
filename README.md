# Starter Flask App v2 (UI + /predict compat)

- ✅ Homepage form at `/`
- ✅ API at `/api/predict` **and** `/predict`
- ✅ CORS enabled (frontend from other origins can call)
- ✅ 50MB upload cap

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
# http://127.0.0.1:5000
```

## Deploy (Render)
- Build: `pip install -r requirements.txt`
- Start: `python app.py`
- Env: `PYTHONUNBUFFERED=1`
