import math
from PIL import Image, ImageOps

logo_path = "LHBロゴ.jpg"
building_path = "LP川口並木.jpg"

SIZE = (600, 338)
OUTPUT = "output.gif"

# ---- モバイル向け ----
frame_duration_ms = 90
logo_hold_frames = 10
slide_frames = 10
building_hold_frames = 18

BG = (255, 255, 255, 255)

def ease_in_out(t: float) -> float:
    """0〜1 を なめらかな加減速に変換"""
    return 0.5 - 0.5 * math.cos(math.pi * t)

def resize_contain(path: str) -> Image.Image:
    """
    画像全体を必ず表示（切らない）
    余白は背景色(BG)で埋める
    """
    img = Image.open(path).convert("RGBA")
    img.thumbnail(SIZE, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", SIZE, BG)
    x = (SIZE[0] - img.width) // 2
    y = (SIZE[1] - img.height) // 2
    canvas.paste(img, (x, y), img)
    return canvas

def resize_cover(path: str) -> Image.Image:
    """
    画面いっぱいに表示（多少のトリミングOK）
    """
    img = Image.open(path).convert("RGBA")
    return ImageOps.fit(img, SIZE, centering=(0.5, 0.5))

def make_slide_left(a: Image.Image, b: Image.Image, steps: int):
    frames = []
    for i in range(steps):
        t = ease_in_out((i + 1) / steps)
        offset = int(SIZE[0] * t)

        frame = Image.new("RGBA", SIZE, BG)
        frame.paste(a, (-offset, 0), a)
        frame.paste(b, (SIZE[0] - offset, 0), b)
        frames.append(frame)
    return frames

# ロゴは切らない、外観は迫力重視
logo = resize_contain(logo_path)
building = resize_cover(building_path)

frames = []

# ロゴ静止
for _ in range(logo_hold_frames):
    frame = Image.new("RGBA", SIZE, BG)
    frame.paste(logo, (0, 0), logo)
    frames.append(frame)

# ロゴ→外観（左スライド）
frames.extend(make_slide_left(logo, building, slide_frames))

# 外観静止
for _ in range(building_hold_frames):
    frame = Image.new("RGBA", SIZE, BG)
    frame.paste(building, (0, 0), building)
    frames.append(frame)

# 外観→ロゴ（左方向でループ）
frames.extend(make_slide_left(building, logo, slide_frames))

# 色数削減（携帯・メルマガ向け）
frames_p = [
    f.convert("P", palette=Image.Palette.ADAPTIVE, colors=128)
    for f in frames
]

frames_p[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames_p[1:],
    duration=frame_duration_ms,
    loop=0,
    disposal=2,
    optimize=False,
)

print("GIF created:", OUTPUT)
