import argparse
from pathlib import Path

import requests


def download_file(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        downloaded = 0

        with output.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                file.write(chunk)
                downloaded += len(chunk)

                if total:
                    percent = downloaded / total * 100
                    print(f"\rDownloaded: {percent:.1f}%", end="")

    print(f"\nSaved to: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download a dataset archive from a supplied URL."
    )
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    download_file(args.url, args.output)
