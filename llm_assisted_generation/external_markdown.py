import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_FILE = BASE_DIR / "data" / "external-sources" / "sources.json"
OUTPUT_DIR = BASE_DIR / "data" / "external-sources" / "downloaded"


def fetch_sources():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sources = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))

    for source in sources:
        name = source["name"]
        url = source["url"]

        output_path = OUTPUT_DIR / f"{name}.md"

        print(f"Downloading {name}...")

        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read().decode("utf-8", errors="ignore")

            output_path.write_text(content, encoding="utf-8")
            print(f"Saved: {output_path}")

        except Exception as error:
            print(f"Failed: {name} -> {error}")


if __name__ == "__main__":
    fetch_sources()