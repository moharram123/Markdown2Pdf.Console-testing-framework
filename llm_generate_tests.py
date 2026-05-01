#!/usr/bin/env python3
"""
LLM-powered Markdown test document generator.
Generates technical documentation Markdown files using OpenAI API,
then auto-creates JSON baselines for the integration test suite.
"""
import argparse
import json
import re
import time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_MD = BASE_DIR / "data" / "llm_generated"
OUTPUT_BL = BASE_DIR / "data" / "baselines"
OUTPUT_MD.mkdir(parents=True, exist_ok=True)
OUTPUT_BL.mkdir(parents=True, exist_ok=True)

client = OpenAI()

TOPICS = [
    "Docker", "Linux", "Git", "PostgreSQL", "Redis", "Nginx",
    "Python", "Rust", "TypeScript", "GraphQL", "REST API", "GitHub Actions",
    "Terraform", "Prometheus", "Grafana", "ElasticSearch", "MongoDB",
    "RabbitMQ", "Kafka", "Flask", "Django", "React", "Vue", "Angular",
    "JWT Authentication", "OAuth2", "WebSockets", "gRPC", "OpenAPI",
    "AWS Lambda", "Azure Functions", "Python FastAPI", "Kubernetes", "Helm",
    "Vault", "Consul", "MinIO", "Argo CD", "Jenkins", "GitHub Copilot",
    "pytest", "Docnado", "OpenTelemetry", "Jaeger", "Istio", "Linkerd",
    "Caddy", "Traefik", "Lexicon API", "Durable Functions",
]

SYSTEM_PROMPT = """You are a technical documentation writer.
Generate a Markdown document about the given topic. The document MUST contain ALL of:
- At least 2 level-1 headings (starting with #)
- At least 1 Markdown table with at least 2 data rows
- At least 1 unordered list with at least 3 items (lines starting with - or *)
- At least 1 fenced code block using ``` with some content inside
Output ONLY raw Markdown content, no explanations or wrapper text."""


def extract_baseline(md: str) -> dict:
    headings = re.findall(r"^#{1,3}\s+(.+)$", md, re.MULTILINE)
    cells = []
    in_table = False
    for line in md.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and "---" not in stripped:
            cols = [c.strip() for c in stripped.strip("|").split("|") if c.strip()]
            if cols and not in_table:
                in_table = True
            if cols:
                cells.extend(cols[1:] if len(cols) > 1 else cols)
        elif not stripped.startswith("|") and in_table:
            in_table = False
    lists = re.findall(r"^[-*+]\s+(.+)$", md, re.MULTILINE)
    code_tokens = []
    for block in re.findall(r"```(?:\w+)?\n([\s\S]+?)```", md):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if lines:
            code_tokens.append(lines[0][:50])
    return {
        "headings": headings[:6],
        "tables": cells[:6],
        "lists": lists[:6],
        "codeblocks": code_tokens[:3],
    }


def generate_one(topic: str, index: int) -> dict | None:
    slug = topic.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
    md_path = OUTPUT_MD / f"llm_{index:03d}_{slug}.md"
    bl_path = OUTPUT_BL / f"llm_{index:03d}_{slug}.json"
    if md_path.exists():
        print(f"  [skip] {md_path.name}")
        return {"status": "skipped"}
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Topic: {topic}"},
            ],
            temperature=0.8,
            max_tokens=900,
        )
        md = r.choices[0].message.content.strip()
    except Exception as e:
        print(f"  [error] {topic}: {e}")
        return None
    bl = extract_baseline(md)
    md_path.write_text(md, encoding="utf-8")
    bl_path.write_text(json.dumps(bl, indent=2), encoding="utf-8")
    print(f"  [ok] {md_path.name}  H:{len(bl['headings'])} T:{len(bl['tables'])} L:{len(bl['lists'])} C:{len(bl['codeblocks'])}")
    return {"status": "generated"}


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown test documents using OpenAI")
    parser.add_argument("--count", type=int, default=50, help="Number of documents to generate")
    args = parser.parse_args()
    count = min(args.count, len(TOPICS))
    print(f"Generating {count} documents...")
    for i, topic in enumerate(TOPICS[:count], 1):
        print(f"[{i:02d}/{count}] {topic}")
        generate_one(topic, i)
        time.sleep(0.3)


if __name__ == "__main__":
    main()
