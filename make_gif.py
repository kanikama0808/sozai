import math
import os
from PIL import Image, ImageOps

# ===== 入力ファイル =====
LOGO_PATH = "LHBロゴ.jpg"
BUILDING_PATH = "LP川口並木.jpg"

BG = (255, 255, 255, 255)  # 白背景（メール＆残像対策）

def ease_in_out(t: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * t)

def resize_contain(path: str, size: tuple[int, int]) -> Image.Image:
    """画像全体を必ず表示（切らない）。余白はBGで埋める。"""
    img = Image.open(path).convert("RGBA")
    img.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, BG)
    x = (size[0] - img.width) // 2
    y = (size[1] - img.height) // 2
    canvas.paste(img, (x, y), img)
    return canvas

def resize_cover(path: str, size: tuple[int, int]) -> Image.Image:
    """画面いっぱいに表示（多少のトリミングOK）。"""
    img = Image.open(path).convert("RGBA")
    return ImageOps.fit(img, size, centering=(0.5, 0.5))

def make_slide_left(a: Image.Image, b: Image.Image, size: tuple[int, int], steps: int) -> list[Image.Image]:
    """aが左へ抜け、右からbが入る（左スライド）"""
    w, h = size
    out = []
    for i in range(steps):
        t = ease_in_out((i + 1) / steps)
        offset = int(w * t)
        frame = Image.new("RGBA", (w, h), BG)
        frame.paste(a, (-offset, 0), a)
        frame.paste(b, (w - offset, 0), b)
        out.append(frame)
    return out

def build_gif(
    out_path: str,
    size: tuple[int, int],
    colors: int,
    frame_duration_ms: int,
    logo_hold_frames: int,
    slide_frames: int,
    building_hold_frames: int,
) -> None:
    logo = resize_contain(LOGO_PATH, size)     # ロゴは切らない
    building = resize_cover(BUILDING_PATH, size)  # 外観は迫力優先

    frames: list[Image.Image] = []

    # ロゴ静止
    for _ in range(logo_hold_frames):
        frame = Image.new("RGBA", size, BG)
        frame.paste(logo, (0, 0), logo)
        frames.append(frame)

    # ロゴ→外観（左スライド）
    frames.extend(make_slide_left(logo, building, size, slide_frames))

    # 外観静止
    for _ in range(building_hold_frames):
        frame = Image.new("RGBA", size, BG)
        frame.paste(building, (0, 0), building)
        frames.append(frame)

    # 外観→ロゴ（左スライドでループ）
    frames.extend(make_slide_left(building, logo, size, slide_frames))

    # 色数削減（容量削減）
    frames_p = [f.convert("P", palette=Image.Palette.ADAPTIVE, colors=colors) for f in frames]

    frames_p[0].save(
        out_path,
        save_all=True,
        append_images=frames_p[1:],
        duration=frame_duration_ms,
        loop=0,          # 無限ループ
        disposal=2,      # 残像対策
        optimize=False,  # 残像リスク回避（必要ならTrue試してOK）
    )

    kb = os.path.getsize(out_path) / 1024
    print(f"created: {out_path}  ({kb:.1f} KB)")

def main():
    # ===== 500KB版（本命） =====
    build_gif(
        out_path="output_500kb.gif",
        size=(540, 304),
        colors=64,
        frame_duration_ms=110,
        logo_hold_frames=8,
        slide_frames=8,
        building_hold_frames=14,
    )

    # ===== 100KB版（超軽量） =====
    build_gif(
        out_path="output_100kb.gif",
        size=(360, 202),
        colors=16,
        frame_duration_ms=140,
        logo_hold_frames=6,
        slide_frames=4,
        building_hold_frames=10,
    )

if __name__ == "__main__":
    main()
