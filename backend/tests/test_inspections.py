import os
from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


client = TestClient(app)


@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Requires PostgreSQL and a trained best.pt model.",
)
def test_create_inspection():
    image = Image.new("RGB", (640, 480), "white")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    response = client.post(
        "/api/v1/inspections",
        files={"file": ("road.jpg", buffer, "image/jpeg")},
    )

    assert response.status_code == 201
    assert "id" in response.json()
