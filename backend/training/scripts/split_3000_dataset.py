from pathlib import Path
import random
import shutil

SOURCE_IMAGES = Path(
    "data/rdd3000/data/images/train/shard_000"
)

SOURCE_LABELS = Path(
    "data/rdd3000/data/labels/train/shard_000"
)

OUTPUT = Path("data/final_3000")

TRAIN_COUNT = 2200
VAL_COUNT = 400
TEST_COUNT = 400

SEED = 42


def copy_pair(image_path, split):

    label_path = SOURCE_LABELS / f"{image_path.stem}.txt"

    image_output = OUTPUT / "images" / split
    label_output = OUTPUT / "labels" / split

    image_output.mkdir(
        parents=True,
        exist_ok=True
    )

    label_output.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy2(
        image_path,
        image_output / image_path.name
    )

    shutil.copy2(
        label_path,
        label_output / label_path.name
    )


images = [
    image
    for image in SOURCE_IMAGES.glob("*.jpg")
    if (SOURCE_LABELS / f"{image.stem}.txt").exists()
]

print("Matching pairs:", len(images))

if len(images) != 3000:
    raise RuntimeError(
        f"Expected 3000 pairs, found {len(images)}"
    )

random.seed(SEED)
random.shuffle(images)

train = images[:2200]

val = images[
    2200:
    2600
]

test = images[
    2600:
    3000
]

for image in train:
    copy_pair(image, "train")

for image in val:
    copy_pair(image, "val")

for image in test:
    copy_pair(image, "test")

print()
print("Split complete")
print("Train:", len(train))
print("Validation:", len(val))
print("Test:", len(test))