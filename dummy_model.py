import hashlib, math, random

def _seed_from_content(data: bytes) -> int:
    h = hashlib.sha256(data).hexdigest()
    return int(h[:8], 16)

def predict_from_bytes(blob: bytes, filename: str):
    seed = _seed_from_content(blob + filename.encode("utf-8"))
    random.seed(seed)
    categories = ["Safe", "Warning", "Danger"]
    cat = random.choice(categories)
    score = round(random.uniform(0.1, 0.95), 2)
    return {"type": "file", "filename": filename, "category": cat, "score": score}

def predict_from_text(text: str):
    n = len(text.strip())
    score = round(1 / (1 + math.exp(-(n - 20)/10)), 2)
    label = "Positive" if score >= 0.5 else "Neutral"
    return {"type": "text", "chars": n, "label": label, "score": score}
