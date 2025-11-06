from PIL import Image
from collections import Counter
import os

def dominant_brand_green(image_path: str) -> str:
    img = Image.open(image_path).convert("RGBA")
    pixels = [p[:3] for p in img.getdata() if p[3] > 0]
    counts = Counter(pixels)

    def is_grey_or_white_or_black(rgb):
        r, g, b = rgb
        if r < 10 and g < 10 and b < 10:
            return True  # near black
        if r > 245 and g > 245 and b > 245:
            return True  # near white
        if abs(r - g) < 5 and abs(g - b) < 5:
            return True  # near grey
        return False

    filtered = [(cnt, rgb) for rgb, cnt in counts.items() if not is_grey_or_white_or_black(rgb)]
    if filtered:
        rgb = max(filtered, key=lambda t: t[0])[1]
    else:
        rgb = counts.most_common(1)[0][0]
    return "#%02X%02X%02X" % rgb


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(here, os.pardir))
    image_path = os.path.join(project_root, "frontend", "public", "Logo-Icon-Green.png")
    print(dominant_brand_green(image_path))