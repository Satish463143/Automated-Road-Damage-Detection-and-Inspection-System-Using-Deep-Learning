from app.ml.detector import detector


def test_detector_availability_returns_boolean():
    assert isinstance(detector.is_available(), bool)
