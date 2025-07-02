import json
from PIL import Image, ImageDraw, ImageFont
import sys

PIXEL_SIZE = 20

def load_grid(filename="grid.json"):
    with open(filename) as f:
        return json.load(f)

def save_grid(grid, filename="grid.json"):
    with open(filename, "w") as f:
        json.dump(grid, f, indent=2)

def generate_image(grid, output="grid.png"):
    width = grid["width"]
    height = grid["height"]
    pixels = grid["pixels"]

    img_width = width * PIXEL_SIZE
    img_height = height * PIXEL_SIZE

    img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))

    for coord, colour in pixels.items():
        x, y = map(int, coord.split(","))
        r, g, b = tuple(int(colour.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        for dx in range(PIXEL_SIZE):
            for dy in range(PIXEL_SIZE):
                img.putpixel((x * PIXEL_SIZE + dx, y * PIXEL_SIZE + dy), (r, g, b, 255))

    draw = ImageDraw.Draw(img)
    line_colour = (255, 255, 255, 100)

    for x in range(width + 1):
        x_pos = x * PIXEL_SIZE
        draw.line([(x_pos, 0), (x_pos, img_height)], fill=line_colour, width=1)

    for y in range(height + 1):
        y_pos = y * PIXEL_SIZE
        draw.line([(0, y_pos), (img_width, y_pos)], fill=line_colour, width=1)

    font = ImageFont.load_default()
    for x in range(width):
        draw.text((x * PIXEL_SIZE + 3, 0), str(x), fill=(255, 255, 255, 100), font=font)
    for y in range(height):
        draw.text((0, y * PIXEL_SIZE + 3), str(y), fill=(255, 255, 255, 100), font=font)

    img.save(output)
    print(f"Saved grid image with transparency and grid lines to {output}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python update_grid.py <x> <y> <#RRGGBB>")
        sys.exit(1)

    try:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        colour = sys.argv[3]
    except ValueError:
        print("Invalid arguments. x and y must be integers, colour must be hex.")
        sys.exit(1)

    if not (colour.startswith("#") and len(colour) == 7):
        print("Colour must be in #RRGGBB format.")
        sys.exit(1)

    grid = load_grid()

    if not (0 <= x < grid["width"] and 0 <= y < grid["height"]):
        print(f"Out-of-bounds pixel: ({x},{y})")
        sys.exit(1)

    grid["pixels"][f"{x},{y}"] = colour
    print(f"Applied pixel update: ({x},{y}) -> {colour}")

    save_grid(grid)
    generate_image(grid)

if __name__ == "__main__":
    main()