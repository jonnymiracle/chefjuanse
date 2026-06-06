import re
import base64
import os

input_file = "index final .html"
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

with open(input_file, "r", encoding="utf-8") as f:
    html = f.read()

pattern = r'src="data:image/(jpeg|png|webp|gif);base64,([^"]+)"'
matches = list(re.finditer(pattern, html))

print(f"Found {len(matches)} images")

replacements = []
seen = {}

for i, m in enumerate(matches):
    ext = m.group(1)
    b64 = m.group(2)

    # Deduplicate: reuse filename if same data
    if b64 in seen:
        fname = seen[b64]
    else:
        fname = f"img_{i+1:02d}.{ext}"
        seen[b64] = fname
        path = os.path.join(output_dir, fname)
        with open(path, "wb") as imgf:
            imgf.write(base64.b64decode(b64))
        size_kb = os.path.getsize(path) / 1024
        print(f"  Saved {fname} ({size_kb:.1f} KB)")

    replacements.append((m.start(), m.end(), f'src="images/{fname}"'))

# Apply replacements in reverse order to preserve offsets
new_html = html
for start, end, repl in reversed(replacements):
    new_html = new_html[:start] + repl + new_html[end:]

with open(input_file, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"\nDone. HTML updated.")
orig_kb = len(html.encode()) / 1024
new_kb = len(new_html.encode()) / 1024
print(f"HTML size: {orig_kb:.0f} KB -> {new_kb:.0f} KB")
