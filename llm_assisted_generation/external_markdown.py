"""
Automatically discover and download external Markdown sources.

This script searches public GitHub repositories for README.md files and
downloads a limited number of Markdown documents. These documents are later
used as input for LLM-assisted test generation.
"""

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SOURCES_DIR = BASE_DIR / "data" / "external-sources"
DOWNLOAD_DIR = SOURCES_DIR / "downloaded"
METADATA_FILE = SOURCES_DIR / "metadata.json"

MAX_SOURCES = 12

SEARCH_QUERIES = [
    "markdown documentation",
    "python documentation",
    "cli tool markdown",
    "developer guide markdown",
]


def safe_name(text: str) -> str:
    name = text.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")
    return name[:80] or "source"


def github_search_repositories(query: str, limit: int = 10) -> list[dict]:
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page={limit}"

    print(f"Searching GitHub for: {query}")

    try:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "markdown2pdf-thesis-test-generator",
            },
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8", errors="ignore"))

        return data.get("items", [])

    except Exception as error:
        print(f"GitHub search failed for '{query}': {error}")
        return []


def build_raw_readme_url(repository: dict) -> str:
    full_name = repository["full_name"]
    default_branch = repository.get("default_branch", "main")
    return f"https://raw.githubusercontent.com/{full_name}/{default_branch}/README.md"


def download_file(url: str, output_path: Path) -> bool:
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "markdown2pdf-thesis-test-generator"},
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read().decode("utf-8", errors="ignore")

        if len(content.strip()) < 300:
            print(f"SKIPPED: source too short -> {url}")
            return False

        output_path.write_text(content, encoding="utf-8")
        return True

    except Exception as error:
        print(f"FAILED download: {url} -> {error}")
        return False


def discover_sources() -> list[dict]:
    discovered = {}

    for query in SEARCH_QUERIES:
        repositories = github_search_repositories(query)

        for repo in repositories:
            full_name = repo.get("full_name")

            if not full_name or full_name in discovered:
                continue

            discovered[full_name] = {
                "name": safe_name(full_name.replace("/", "_")),
                "repository": full_name,
                "stars": repo.get("stargazers_count", 0),
                "url": build_raw_readme_url(repo),
            }

            print(f"  Found: {full_name}")

            if len(discovered) >= MAX_SOURCES:
                return list(discovered.values())

    return list(discovered.values())


def main() -> None:
    print("=" * 60)
    print("AUTOMATIC MARKDOWN SOURCE DISCOVERY")
    print("=" * 60)

    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    sources = discover_sources()

    if not sources:
        raise RuntimeError("No external Markdown sources were discovered.")

    downloaded_sources = []

    print(f"\nDownloading up to {len(sources)} Markdown source file(s)...")

    for source in sources:
        output_path = DOWNLOAD_DIR / f"{source['name']}.md"

        print(f"Downloading: {source['repository']}")

        if download_file(source["url"], output_path):
            source["local_file"] = str(output_path)
            downloaded_sources.append(source)
            print(f"  SAVED: {output_path.name}")

    METADATA_FILE.write_text(
        json.dumps(downloaded_sources, indent=2),
        encoding="utf-8",
    )

    print(f"\nDownloaded {len(downloaded_sources)} Markdown file(s).")
    print(f"Metadata saved to: {METADATA_FILE}")

    if len(downloaded_sources) < 10:
        print("Warning: fewer than 10 sources were downloaded. Generated test count may be lower than expected.")


if __name__ == "__main__":
    main()