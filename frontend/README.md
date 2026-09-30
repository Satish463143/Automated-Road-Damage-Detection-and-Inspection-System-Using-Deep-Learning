# Road Damage Detection Frontend

React dashboard for the Road Damage and Pothole Detection System.

It connects to the FastAPI backend and provides:

- Dashboard analytics
- Road image upload
- Image detection result
- Original vs annotated image comparison
- Damage counts
- Detection table
- Inspection history
- Inspection details
- Delete inspection
- Model performance information
- Backend/database/model health status

## Stack

- React 19
- Vite 8
- React Router 7
- Native browser `fetch`
- Plain responsive CSS

## 1. Requirements

Vite 8 requires a recent Node.js version.

Use Node.js 20.19+ or 22.12+.

Check:

```bash
node -v
npm -v
```

## 2. Install packages

From the frontend folder:

```bash
npm install
```

## 3. Create .env

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Default `.env`:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_APP_NAME=Road Damage Inspection
```

## 4. Start the backend first

The FastAPI backend should run at:

```text
http://127.0.0.1:8000
```

Backend command:

```bash
uvicorn app.main:app --reload
```

## 5. Start React

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

## 6. Frontend pages

```text
/                       Dashboard
/inspect                Upload and inspect a road image
/inspections            Inspection history
/inspections/:id        Single inspection details
/model                  Model performance
```

## 7. Backend endpoints used

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

## 8. Source structure

```text
src/
├── components/
│   ├── dashboard/
│   ├── inspection/
│   ├── layout/
│   └── ui/
├── config/
├── data/
├── hooks/
├── pages/
├── services/
├── styles/
└── utils/
```

## 9. Image inspection flow

```text
Select road image
        ↓
React validates basic file type and size
        ↓
POST multipart image to FastAPI
        ↓
FastAPI stores original image
        ↓
YOLO runs detection
        ↓
Backend stores annotated image
        ↓
PostgreSQL stores inspection and detection records
        ↓
React receives JSON
        ↓
Dashboard shows result
```

## 10. Important

The frontend does not:

- Run YOLO
- Connect directly to PostgreSQL
- Store inspection records itself

All ML and database work stays inside the FastAPI backend.
