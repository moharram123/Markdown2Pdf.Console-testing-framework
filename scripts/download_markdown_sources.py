#!/usr/bin/env python3
"""
Download Markdown sources from GitHub and other sources.
"""

import os
import re
import json
import requests
from pathlib import Path
from datetime import datetime


class MarkdownSourceDownloader:
    def __init__(self):
        self.sources_dir = Path("data/sources")
        self.sources_dir.mkdir(parents=True, exist_ok=True)
        self.metadata = []
    
    def download_from_urls(self, urls):
        """Download Markdown files from direct URLs with unique names."""
        print(f"Downloading {len(urls)} files...")
        
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                # Extract repository owner and name for unique filename
                match = re.search(r'github\.com/([^/]+)/([^/]+)/', url)
                if match:
                    owner = match.group(1)
                    repo = match.group(2)
                    filename = f"{owner}_{repo}.md"
                else:
                    filename = url.split('/')[-1]
                
                filepath = self.sources_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                self.metadata.append({
                    "filename": filename,
                    "source_url": url,
                    "downloaded_at": datetime.now().isoformat(),
                    "size": len(response.text)
                })
                
                print(f"  Downloaded: {filename}")
            
            except Exception as e:
                print(f"  Error downloading {url}: {e}")
    
    def search_github(self, query="documentation", language="markdown"):
        """Search GitHub for Markdown repositories."""
        print(f"Searching GitHub for: {query}...")
        
        headers = {"Accept": "application/vnd.github.v3+json"}
        url = f"https://api.github.com/search/repositories?q={query}+language:{language}&sort=stars&per_page=50"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            repos = response.json().get("items", [])
            
            urls = []
            for repo in repos:
                readme_url = f"https://raw.githubusercontent.com/{repo['full_name']}/main/README.md"
                urls.append(readme_url)
                print(f"  Found: {repo['full_name']}")
            
            return urls
        
        except Exception as e:
            print(f"  Error searching GitHub: {e}")
            return []
    
    def search_markdown_sources(self, query="markdown"):
        """Use sample Markdown sources as fallback."""
        print(f"Searching for: {query}...")
        
        sample_sources = [
            "https://raw.githubusercontent.com/adam-p/markdown-here/master/README.md",
        ]
        
        return sample_sources
    
    def save_metadata(self):
        """Save metadata about downloaded files."""
        metadata_file = self.sources_dir / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        print(f"Metadata saved to {metadata_file}")


def main():
    downloader = MarkdownSourceDownloader()
    
    print("=" * 60)
    print("MARKDOWN SOURCE DOWNLOADER")
    print("=" * 60)
    
    print("\nSearching GitHub...")
    github_sources = downloader.search_github(query="documentation")
    
    print("\nUsing sample sources...")
    sample_sources = downloader.search_markdown_sources()
    
    all_sources = github_sources + sample_sources
    
    if all_sources:
        print(f"\nDownloading {len(all_sources)} files...")
        downloader.download_from_urls(all_sources)
        downloader.save_metadata()
        print(f"\nDownloaded {len(downloader.metadata)} sources")
    else:
        print("No sources found")


if __name__ == "__main__":
    main()