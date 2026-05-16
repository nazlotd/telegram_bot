from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE = BASE_DIR / "data" / "intro.jpeg"
OUTPUT = BASE_DIR / "data" / "intro.gif"

SIZE = 640
FRAME_COUNT = 36
DURATION_MS = 55


def center_crop_square(image):
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side))


def make_frame(base, index):
    progress = index / (FRAME_COUNT - 1)
    wave = 1 - abs((progress * 2) - 1)
    scale = 1.0 + (0.08 * wave)
    brightness = 1.0 + (0.12 * wave)
    contrast = 1.02 + (0.08 * wave)

    scaled_size = round(SIZE * scale)
    frame = base.resize((scaled_size, scaled_size), Image.Resampling.LANCZOS)

    left = (scaled_size - SIZE) // 2
    top = (scaled_size - SIZE) // 2
    frame = frame.crop((left, top, left + SIZE, top + SIZE))

    glow = frame.filter(ImageFilter.GaussianBlur(radius=8))
    glow = ImageEnhance.Brightness(glow).enhance(1.25 + (0.35 * wave))
    frame = Image.blend(glow, frame, 0.82)
    frame = ImageEnhance.Brightness(frame).enhance(brightness)
    frame = ImageEnhance.Contrast(frame).enhance(contrast)

    return frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=128)


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source image not found: {SOURCE}")

    base = Image.open(SOURCE).convert("RGB")
    base = center_crop_square(base).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    frames = [make_frame(base, index) for index in range(FRAME_COUNT)]

    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
    )

    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
