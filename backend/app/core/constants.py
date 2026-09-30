DAMAGE_CLASS_MAP = {
    0: {"code": "D00", "name": "Longitudinal Crack"},
    1: {"code": "D10", "name": "Transverse Crack"},
    2: {"code": "D20", "name": "Alligator Crack"},
    3: {"code": "D40", "name": "Pothole"},
}

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

INSPECTION_STATUS_PROCESSING = "processing"
INSPECTION_STATUS_COMPLETED = "completed"
INSPECTION_STATUS_FAILED = "failed"
