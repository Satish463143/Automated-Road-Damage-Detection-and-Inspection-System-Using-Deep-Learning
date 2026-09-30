def calculate_box_area(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> float:
    width = max(0.0, x2 - x1)
    height = max(0.0, y2 - y1)
    return width * height
