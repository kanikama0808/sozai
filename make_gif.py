from PIL import Image, ImageOps

logo_path = "LHBロゴ.png"
building_path = "LP川口並木.jpg"

SIZE = (600, 338)

logo = Image.open(logo_path).convert("RGBA")
building = Image.open(building_path).convert("RGBA")

logo = ImageOps.fit(logo, SIZE, centering=(0.5, 0.5))
building = ImageOps.fit(building, SIZE, centering=(0.5, 0.5))

frames = []
frame_duration_ms = 100

logo_hold_frames = 10  # 1.0秒
slide_frames = 6  # 0.6秒
building_hold_frames = 20  # 2.0秒

for _ in range(logo_hold_frames):
    frames.append(logo.copy())

for i in range(slide_frames):
    t = (i + 1) / slide_frames
    offset = int(SIZE[0] * t)
    frame = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    frame.paste(logo, (-offset, 0))
    frame.paste(building, (SIZE[0] - offset, 0))
    frames.append(frame)

for _ in range(building_hold_frames):
    frames.append(building.copy())

frames[0].save(
    "output.gif",
    save_all=True,
    append_images=frames[1:],
    duration=frame_duration_ms,
    loop=0,
    optimize=True,
)

print("GIF created: output.gif")
