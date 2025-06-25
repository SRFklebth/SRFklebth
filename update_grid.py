import json
from PIL import Image, ImageDraw, ImageFont
import os

GRID_SIZE_X = 101
GRID_SIZE_Y = 51
PIXEL_SIZE = 20

def load_grid(filename="grid.json"):
    with open(filename) as f:
        return json.load(f)

def save_grid(grid, filename="grid.json"):
    with open(filename, "w") as f:
        json.dump(grid, f, indent=2)

def merge_updates(grid, updates_folder="pixel-updates"):
    for fname in os.listdir(updates_folder):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(updates_folder, fname)
        with open(path) as f:
            update = json.load(f)
        x, y = update.get("x"), update.get("y")
        color = update.get("color")

        if not (isinstance(x, int) and isinstance(y, int) and isinstance(color, str)):
            print(f"Skipping invalid update file: {fname} (bad format)")
            continue

        if not (0 <= x < grid["width"] and 0 <= y < grid["height"]):
            print(f"Skipping out-of-bounds pixel in file: {fname} ({x},{y})")
            continue

        if not (color.startswith("#") and len(color) == 7):
            print(f"Skipping invalid color format in file: {fname} ({color})")
            continue

        grid["pixels"][f"{x},{y}"] = color
        print(f"Applied pixel update from {fname}: ({x},{y}) -> {color}")

    return grid

def generate_image(grid, output="grid.png"):
    width = grid["width"]
    height = grid["height"]
    pixels = grid["pixels"]

    img_width = width * PIXEL_SIZE
    img_height = height * PIXEL_SIZE

    # Create an RGBA image with transparent background
    img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))

    # Draw colored pixels
    for coord, color in pixels.items():
        x, y = map(int, coord.split(","))
        r, g, b = tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        for dx in range(PIXEL_SIZE):
            for dy in range(PIXEL_SIZE):
                img.putpixel((x * PIXEL_SIZE + dx, y * PIXEL_SIZE + dy), (r, g, b, 255))

    # Draw grid lines on top
    draw = ImageDraw.Draw(img)
    line_color = (255, 255, 255, 100)  # semi-transparent black lines

    # Vertical lines
    for x in range(width + 1):
        x_pos = x * PIXEL_SIZE
        draw.line([(x_pos, 0), (x_pos, img_height)], fill=line_color, width=1)

    # Horizontal lines
    for y in range(height + 1):
        y_pos = y * PIXEL_SIZE
        draw.line([(0, y_pos), (img_width, y_pos)], fill=line_color, width=1)

    # Optional: Add coordinate numbers (x,y) along axes
    # This requires a font file; will use default font if available.
    try:
        font = ImageFont.load_default()
        # Draw x coordinates on top
        for x in range(width):
            draw.text((x * PIXEL_SIZE + 3, 0), str(x), fill=(255, 255, 255, 100), font=font)
        # Draw y coordinates on left side
        for y in range(height):
            draw.text((0, y * PIXEL_SIZE + 3), str(y), fill=(255, 255, 255, 100), font=font)
    except Exception:
        pass  # If font loading fails, skip

    img.save(output)
    print(f"Saved grid image with transparency and grid lines to {output}")

if __name__ == "__main__":
    grid = load_grid()
    grid = merge_updates(grid)
    save_grid(grid)
    generate_image(grid)
