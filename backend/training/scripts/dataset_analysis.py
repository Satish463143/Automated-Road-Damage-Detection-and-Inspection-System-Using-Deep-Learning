import argparse
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


VALID_CLASSES = {"D00", "D10", "D20", "D40"}


def analyze(annotations_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    class_counts = Counter()
    objects_per_image = []
    box_areas = []
    rows = []

    xml_files = list(annotations_dir.rglob("*.xml"))

    for xml_path in xml_files:
        root = ET.parse(xml_path).getroot()

        size = root.find("size")
        image_width = int(size.findtext("width", default="0"))
        image_height = int(size.findtext("height", default="0"))

        object_count = 0

        for obj in root.findall("object"):
            class_name = obj.findtext("name", default="").strip()
            if class_name not in VALID_CLASSES:
                continue

            bbox = obj.find("bndbox")
            xmin = float(bbox.findtext("xmin", default="0"))
            ymin = float(bbox.findtext("ymin", default="0"))
            xmax = float(bbox.findtext("xmax", default="0"))
            ymax = float(bbox.findtext("ymax", default="0"))

            area = max(0, xmax - xmin) * max(0, ymax - ymin)

            class_counts[class_name] += 1
            box_areas.append(area)
            object_count += 1

            rows.append(
                {
                    "xml": str(xml_path),
                    "class": class_name,
                    "image_width": image_width,
                    "image_height": image_height,
                    "bbox_area": area,
                }
            )

        objects_per_image.append(object_count)

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(output_dir / "annotations_summary.csv", index=False)

    class_df = pd.DataFrame(
        sorted(class_counts.items()),
        columns=["class", "count"],
    )
    class_df.to_csv(output_dir / "class_counts.csv", index=False)

    if not class_df.empty:
        ax = class_df.plot(
            kind="bar",
            x="class",
            y="count",
            legend=False,
            title="Road Damage Class Distribution",
        )
        ax.set_xlabel("Damage class")
        ax.set_ylabel("Annotations")
        plt.tight_layout()
        plt.savefig(output_dir / "class_distribution.png")
        plt.close()

    if objects_per_image:
        plt.hist(objects_per_image, bins=20)
        plt.title("Objects Per Image")
        plt.xlabel("Number of labeled damages")
        plt.ylabel("Images")
        plt.tight_layout()
        plt.savefig(output_dir / "objects_per_image.png")
        plt.close()

    if box_areas:
        plt.hist(box_areas, bins=30)
        plt.title("Bounding Box Area Distribution")
        plt.xlabel("Area in pixels")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(output_dir / "bbox_area_distribution.png")
        plt.close()

    print(f"XML files: {len(xml_files)}")
    print(f"Damage annotations: {sum(class_counts.values())}")
    print("Class counts:", dict(class_counts))
    print(f"Reports saved to: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotations-dir", required=True, type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/eda"),
    )
    args = parser.parse_args()

    analyze(args.annotations_dir, args.output_dir)
