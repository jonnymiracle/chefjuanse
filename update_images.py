import re

input_file = "index final .html"

with open(input_file, "r", encoding="utf-8") as f:
    html = f.read()

# ── 1. Replace hero slideshow slides ──────────────────────────────────────────
old_slides = (
    '<div class="slide active"><img src="images/img_01.jpeg" alt="Chef Juanse"></div>\n'
    '    <div class="slide"><img src="images/img_02.jpeg" alt="Emplatado en vivo"></div>'
)
new_slides = (
    '<div class="slide active"><img src="images/Hero1.jpg" alt="Chef Juanse"></div>\n'
    '    <div class="slide"><img src="images/Hero2.jpg" alt="Chef Juanse - plato"></div>\n'
    '    <div class="slide"><img src="images/Hero3.jpg" alt="Chef Juanse - experiencia"></div>'
)

if old_slides in html:
    html = html.replace(old_slides, new_slides)
    print("✓ Hero slideshow updated (3 slides)")
else:
    print("✗ Hero slides pattern NOT found — check manually")

# ── 2. Replace photos JS array (base64 → file paths) ─────────────────────────
gallery_files = [
    ("images/IMG_1535.JPG", "Pescado Entero con Flores"),
    ("images/IMG_1536.JPG", "Pulpo a la Brasa"),
    ("images/IMG_1537.JPG", "Salmón Wellington"),
    ("images/IMG_1538.JPG", "Pechuga & Risotto"),
    ("images/IMG_1539.JPG", "Berenjenas Empanadas"),
    ("images/IMG_1540.JPG", "Sardinas & Remolacha"),
    ("images/IMG_1541.JPG", "Pappardelle de Hongos"),
    ("images/IMG_1542.JPG", "Atún & Sandía"),
    ("images/IMG_1543.JPG", "Steak Dorado"),
    ("images/IMG_1544.JPG", "Mesa de Evento"),
    ("images/IMG_1545.JPG", "Bowl Artístico"),
    ("images/IMG_1546.JPG", "Pescado & Espárragos"),
    ("images/IMG_1547.JPG", "Pollo & Risotto"),
    ("images/IMG_1548.JPG", "Ramen de la casa"),
]

new_array_lines = ["const photos = ["]
for path, desc in gallery_files:
    new_array_lines.append(f'  {{ desc: "{desc}", src: "{path}" }},')
new_array_lines[-1] = new_array_lines[-1].rstrip(",")  # remove trailing comma on last
new_array_lines.append("];")
new_photos_block = "\n".join(new_array_lines)

# Match the whole photos array (from "const photos = [" to "];")
pattern = r'const photos = \[.*?\];'
match = re.search(pattern, html, re.DOTALL)
if match:
    html = html[:match.start()] + new_photos_block + html[match.end():]
    print("✓ Gallery photos array updated (14 real images)")
else:
    print("✗ photos array pattern NOT found — check manually")

with open(input_file, "w", encoding="utf-8") as f:
    f.write(html)

size_kb = len(html.encode()) / 1024
print(f"\nHTML size now: {size_kb:.0f} KB")
