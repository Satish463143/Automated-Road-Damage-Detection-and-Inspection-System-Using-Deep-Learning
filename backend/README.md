# Road Damage Detection Backend

FastAPI + PostgreSQL + SQLAlchemy + Alembic + Ultralytics YOLO backend for
image-based road damage inspection.

## Damage classes

- D00: Longitudinal Crack
- D10: Transverse Crack
- D20: Alligator Crack
- D40: Pothole

## 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Create .env

Copy `.env.example` to `.env`.

Windows:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

## 4. Start PostgreSQL

Option A: local PostgreSQL.

Create a database named:

```text
road_damage_db
```

Option B: Docker:

```bash
docker compose -f docker-compose.postgres.yml up -d
```

## 5. Run database migration

```bash
alembic upgrade head
```

## 6. Start FastAPI

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 7. Model file

The API starts without a trained model.

For image detection, place your trained model at:

```text
models/weights/best.pt
```

Then restart the backend.

Check:

```text
GET /api/v1/health
```

The response should show:

```json
{
  "status": "healthy",
  "database": "connected",
  "model": "loaded"
}
```

## 8. Main API endpoints

```text
GET    /api/v1/health
POST   /api/v1/inspections
GET    /api/v1/inspections
GET    /api/v1/inspections/{id}
DELETE /api/v1/inspections/{id}
GET    /api/v1/analytics/summary
GET    /api/v1/analytics/damage-distribution
GET    /api/v1/model
```

## 9. Training workflow

### Analyze Pascal VOC annotations

```bash
python training/scripts/dataset_analysis.py \
  --annotations-dir data/raw/RDD2022/Annotations
```

### Validate source dataset

```bash
python training/scripts/validate_dataset.py \
  --images-dir data/raw/RDD2022/images \
  --annotations-dir data/raw/RDD2022/Annotations
```

### Convert VOC XML to YOLO labels

```bash
python training/scripts/convert_voc_to_yolo.py \
  --images-dir data/raw/RDD2022/images \
  --annotations-dir data/raw/RDD2022/Annotations \
  --output-images data/converted/images \
  --output-labels data/converted/labels
```

### Split into train, validation and test

```bash
python training/scripts/split_dataset.py \
  --images-dir data/converted/images \
  --labels-dir data/converted/labels \
  --output-dir data/processed
```

### Train

```bash
python training/scripts/train.py \
  --data training/configs/road_damage.yaml \
  --model yolov8n.pt \
  --epochs 75 \
  --imgsz 640 \
  --batch 16
```

Copy the best trained weight file to:

```text
models/weights/best.pt
```

### Evaluate on test set

```bash
python training/scripts/evaluate.py \
  --weights models/weights/best.pt \
  --data training/configs/road_damage.yaml
```

After evaluation, update:

```text
models/metadata/model_info.json
```

with your real precision, recall, mAP50 and mAP50-95.

## 10. React frontend

React should call the FastAPI backend.

Main frontend pages:

- Dashboard
- Inspect Road
- Inspection History
- Inspection Details
- Model Performance

The frontend should not connect directly to PostgreSQL and should not run YOLO.
