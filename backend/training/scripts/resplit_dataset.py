from pathlib import Path
import random
import shutil

SOURCE_IMAGES = Path("data/processed/images/train")
SOURCE_LABELS = Path("data/processed/labels/train")

OUTPUT_ROOT = Path("data/final")

TRAIN_COUNT = 695
VAL_COUNT = 100
TEST_COUNT = 200

SEED = 42


def copy_pair(image_path, split):
    label_path = SOURCE_LABELS / f"{image_path.stem}.txt"

    if not label_path.exists():
        return False

    image_output = OUTPUT_ROOT / "images" / split
    label_output = OUTPUT_ROOT / "labels" / split

    image_output.mkdir(parents=True, exist_ok=True)
    label_output.mkdir(parents=True, exist_ok=True)

    shutil.copy2(
        image_path,
        image_output / image_path.name
    )

    shutil.copy2(
        label_path,
        label_output / label_path.name
    )

    return True


images = [
    image
    for image in SOURCE_IMAGES.glob("*.jpg")
    if (SOURCE_LABELS / f"{image.stem}.txt").exists()
]

print("Matching pairs:", len(images))

if len(images) < TRAIN_COUNT + VAL_COUNT + TEST_COUNT:
    raise RuntimeError(
        f"Need {TRAIN_COUNT + VAL_COUNT + TEST_COUNT} pairs, "
        f"but only found {len(images)}"
    )

random.seed(SEED)
random.shuffle(images)

train = images[:TRAIN_COUNT]

val = images[
    TRAIN_COUNT:
    TRAIN_COUNT + VAL_COUNT
]

test = images[
    TRAIN_COUNT + VAL_COUNT:
    TRAIN_COUNT + VAL_COUNT + TEST_COUNT
]

for image in train:
    copy_pair(image, "train")

for image in val:
    copy_pair(image, "val")

for image in test:
    copy_pair(image, "test")

print()
print("Finished")
print("Train:", len(train))
print("Validation:", len(val))
print("Test:", len(test))