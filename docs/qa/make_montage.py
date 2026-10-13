"""Create page contact sheets for visual Word-export inspection."""

from pathlib import Path
import sys
from PIL import Image, ImageDraw

render_name = sys.argv[1] if len(sys.argv) > 1 else "render10"
pages_dir = Path(__file__).parent / render_name / "pages"
pages = sorted(pages_dir.glob("page-*.png"))
for start in range(0, len(pages), 12):
    group = pages[start : start + 12]
    sheet = Image.new("RGB", (4 * 300, 3 * 410), "white")
    draw = ImageDraw.Draw(sheet)
    for pos, path in enumerate(group):
        page = Image.open(path).convert("RGB")
        page.thumbnail((290, 380))
        x = (pos % 4) * 300 + (300 - page.width) // 2
        y = (pos // 4) * 410 + 22
        sheet.paste(page, (x, y))
        draw.text((pos % 4 * 300 + 5, pos // 4 * 410 + 3), path.stem, fill="red")
    sheet.save(pages_dir.parent / f"montage-{start // 12 + 1}.png")
