"""
Prompt and generation logic for LLM-assisted Markdown test cases.
"""


def build_generation_prompt(source_content: str, variant_number: int) -> str:
    return f"""
You are generating Markdown test cases for an automated Markdown-to-PDF integration test framework.

Create one valid CONTROL Markdown file and one faulty REGRESSION Markdown file.

Return exactly this format:

---CONTROL---
<valid markdown>

---REGRESSION---
<faulty markdown>

CONTROL requirements:
- It must be valid Markdown.
- It must be realistic and based loosely on the source document.
- It must contain at least 5 headings using #, ##, or ###.
- It must contain one table with the columns Name and Role.
- The table must include these rows: Alice, Bob, Carol, Dave, Admin.
- It must contain one bullet list with at least 6 items.
- The bullet list must include:
  First item, Second item, Third item, Fourth item, Fifth item, Sixth item.
- It must contain one Python code block containing both print( and def.
- It must contain one JavaScript code block containing console.log.

REGRESSION requirements:
- It must be similar to the control file.
- It must contain exactly one intentional structural defect.
- Choose exactly one of these defects:
  missing heading, missing table row, missing list item, or missing code block.
- Do not explain the defect inside the Markdown file.

Variation instruction:
- This is variant number {variant_number}.
- Make this variant meaningfully different from other variants.
- Change the topic, heading names, list wording, and code examples while keeping the required validation elements.

Important:
- Output only the requested CONTROL and REGRESSION sections.
- Do not include explanations before or after the generated Markdown.

Source document excerpt:
---
{source_content[:2500]}
---
""".strip()


def split_llm_response(content: str) -> tuple[str, str]:
    if "---CONTROL---" not in content or "---REGRESSION---" not in content:
        raise ValueError("LLM response does not contain CONTROL and REGRESSION markers.")

    control = content.split("---CONTROL---", 1)[1].split("---REGRESSION---", 1)[0].strip()
    regression = content.split("---REGRESSION---", 1)[1].strip()

    if not control:
        raise ValueError("Generated control content is empty.")

    if not regression:
        raise ValueError("Generated regression content is empty.")

    return control, regression


def generate_markdown_pair(client, source_content: str, variant_number: int = 1) -> tuple[str, str]:
    for attempt in range(1, 4):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You generate raw Markdown test cases for automated PDF validation.",
                    },
                    {
                        "role": "user",
                        "content": build_generation_prompt(source_content, variant_number),
                    },
                ],
                temperature=0.6,
                max_tokens=2500,
            )

            content = response.choices[0].message.content.strip()
            return split_llm_response(content)

        except Exception as error:
            print(f"Attempt {attempt} failed: {error}")

    raise RuntimeError("LLM generation failed after 3 attempts.")