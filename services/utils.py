import re

def extract_markdown(response: str) -> str:
    """
    Normalise raw AI string into clean Markdown-safe text.
    """

    try:
        # ---- Validate type ----
        if not isinstance(response, str):
            raise TypeError("Response must be a string")

        # ---- Strip outer whitespace ----
        markdown = response.strip()

        if not markdown:
            raise ValueError("Response is empty")

        # ---- Remove leading indentation (from triple-quoted strings) ----
        lines = markdown.splitlines()
        stripped_lines = [line.lstrip() for line in lines]
        markdown = "\n".join(stripped_lines)

        # ---- Normalise line endings ----
        markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")

        # ---- Collapse excessive blank lines ----
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)

        # ---- Normalise bullet points ----
        markdown = re.sub(r"\n\s*-\s*", "\n- ", markdown)

        # ---- Remove trailing whitespace ----
        markdown = re.sub(r"[ \t]+$", "", markdown, flags=re.MULTILINE)

        # ---- Remove non-printable/control chars (except newline + tab) ----
        markdown = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", "", markdown)

        # ---- Final validation ----
        if not markdown:
            raise ValueError("Markdown became empty after cleaning")

        return markdown

    except Exception as e:
        raise RuntimeError(f"Failed to process AI response: {str(e)}")