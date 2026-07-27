import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python clean.py <input_markdown_file>")
    sys.exit(1)

input_file = Path(sys.argv[1])
output_file = Path("docs/manual_cleaned.md")

print("Cleaning:", input_file)
print("Output:", output_file)

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove LaTeX page breaks
text = text.replace("\\newpage", "")

# 2. Remove Table of Contents block
text = re.sub(
    r"## Table of Contents.*?(?=^##\s)",
    "",
    text,
    flags=re.DOTALL | re.MULTILINE
)

# 3. Remove "Back to Table of Contents"
text = re.sub(
    r"\[Back to Table of Contents\]\(#Tabl01\)",
    "",
    text
)

# 4. Convert "\" at end of line to HTML line break
text = re.sub(
    r"\\\s*$",
    "<br>",
    text,
    flags=re.MULTILINE
)

# 5. Remove standalone "\" lines
text = re.sub(
    r"^\s*\\\s*$",
    "",
    text,
    flags=re.MULTILINE
)

# 6. Remove accidental double backslashes
text = text.replace("\\\\", "")

# 7. Clean excessive blank lines
text = re.sub(
    r"\n{3,}",
    "\n\n",
    text
)

# 8. Protect <filename> constructs from Markdown interpretation
text = re.sub(
    r"\\<(.*?)\\>",
    r"`<\1>`",
    text
)

output_file.parent.mkdir(exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaned Markdown written to:", output_file)