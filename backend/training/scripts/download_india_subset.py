from pathlib import Path
import random
import shutil

from huggingface_hub import HfApi, hf_hub_download


REPO_ID = "dronefreak/RDD2022"
REPO_TYPE = "dataset"

OUTPUT_ROOT = Path("data/processed")
CACHE_DIR = Path("data/hf_temp")

SEED = 42

SPLITS = {
    "train": ("train", 2000),
    "valid": ("val", 400),
    "test": ("test", 400),
}


def get_matching_pairs():
    api = HfApi()

    print("Reading dataset file list...")

    repo_files = api.list_repo_files(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
    )

    repo_file_set = set(repo_files)

    pairs_by_split = {}

    for remote_split in SPLITS:
        image_prefix = f"data/images/{remote_split}/"

        india_images = [
            path
            for path in repo_files
            if path.startswith(image_prefix)
            and Path(path).name.startswith("India_")
            and path.lower().endswith(".jpg")
        ]

        matching_pairs = []

        for image_path in india_images:
            label_path = (
                image_path
                .replace("/images/", "/labels/")
                .rsplit(".", 1)[0]
                + ".txt"
            )

            if label_path in repo_file_set:
                matching_pairs.append(
                    (image_path, label_path)
                )

        pairs_by_split[remote_split] = matching_pairs

        print(
            f"{remote_split}: "
            f"{len(matching_pairs)} matching India image/label pairs"
        )

    return pairs_by_split


def download_file(repo_path):
    return Path(
        hf_hub_download(
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            filename=repo_path,
            local_dir=CACHE_DIR,
        )
    )


def prepare_output():
    for _, (local_split, _) in SPLITS.items():
        image_dir = OUTPUT_ROOT / "images" / local_split
        label_dir = OUTPUT_ROOT / "labels" / local_split

        image_dir.mkdir(parents=True, exist_ok=True)
        label_dir.mkdir(parents=True, exist_ok=True)


def download_subset():
    random.seed(SEED)

    pairs_by_split = get_matching_pairs()
    prepare_output()

    for remote_split, (local_split, required_count) in SPLITS.items():

        pairs = pairs_by_split[remote_split]

        if len(pairs) < required_count:
            raise RuntimeError(
                f"Not enough India pairs in {remote_split}. "
                f"Required {required_count}, found {len(pairs)}."
            )

        selected = random.sample(
            pairs,
            required_count,
        )

        print()
        print(
            f"Downloading {required_count} pairs "
            f"for {local_split}..."
        )

        image_output = OUTPUT_ROOT / "images" / local_split
        label_output = OUTPUT_ROOT / "labels" / local_split

        for index, (image_repo_path, label_repo_path) in enumerate(
            selected,
            start=1,
        ):

            image_downloaded = download_file(image_repo_path)
            label_downloaded = download_file(label_repo_path)

            image_destination = (
                image_output / Path(image_repo_path).name
            )

            label_destination = (
                label_output / Path(label_repo_path).name
            )

            shutil.copy2(
                image_downloaded,
                image_destination,
            )

            shutil.copy2(
                label_downloaded,
                label_destination,
            )

            if index % 50 == 0 or index == required_count:
                print(
                    f"{local_split}: "
                    f"{index}/{required_count}"
                )

    print()
    print("Download finished.")


def verify_dataset():

    print()
    print("Verifying dataset...")

    total_images = 0
    total_labels = 0

    for _, (split, expected) in SPLITS.items():

        image_dir = OUTPUT_ROOT / "images" / split
        label_dir = OUTPUT_ROOT / "labels" / split

        images = list(image_dir.glob("*.jpg"))
        labels = list(label_dir.glob("*.txt"))

        image_stems = {file.stem for file in images}
        label_stems = {file.stem for file in labels}

        missing_labels = image_stems - label_stems
        missing_images = label_stems - image_stems

        print()
        print(f"{split}:")
        print(f"  Images: {len(images)}")
        print(f"  Labels: {len(labels)}")
        print(f"  Missing labels: {len(missing_labels)}")
        print(f"  Missing images: {len(missing_images)}")

        if len(images) != expected:
            raise RuntimeError(
                f"{split} should have {expected} images."
            )

        if missing_labels:
            raise RuntimeError(
                f"{split} contains images without labels."
            )

        if missing_images:
            raise RuntimeError(
                f"{split} contains labels without images."
            )

        total_images += len(images)
        total_labels += len(labels)

    print()
    print("--------------------------------")
    print(f"Total images: {total_images}")
    print(f"Total labels: {total_labels}")
    print("--------------------------------")

    if total_images == 2800 and total_labels == 2800:
        print("Dataset verification PASSED.")
    else:
        raise RuntimeError(
            "Dataset verification failed."
        )


if __name__ == "__main__":
    download_subset()
    verify_dataset()