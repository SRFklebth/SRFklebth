import json
from PIL import Image
import os

GRID_SIZE_X = 100
GRID_SIZE_Y = 50
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

    img = Image.new("RGB", (width * PIXEL_SIZE, height * PIXEL_SIZE), "white")

    for coord, color in pixels.items():
        x, y = map(int, coord.split(","))
        r, g, b = tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        for dx in range(PIXEL_SIZE):
            for dy in range(PIXEL_SIZE):
                img.putpixel((x * PIXEL_SIZE + dx, y * PIXEL_SIZE + dy), (r, g, b))

    img.save(output)
    print(f"Saved grid image to {output}")

if __name__ == "__main__":
    grid = load_grid()
    grid = merge_updates(grid)
    save_grid(grid)
    generate_image(grid)
