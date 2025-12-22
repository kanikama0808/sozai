from PIL import Image, ImageOps

logo_path = "LHBロゴ_1120_630.png"
building_path = "LP西川口Ⅱ_外観パース_250522.jpg"

SIZE = (600, 338)

logo = Image.open(logo_path).convert("RGBA")
building = Image.open(building_path).convert("RGBA")

logo = ImageOps.fit(logo, SIZE, centering=(0.5, 0.5))
building = ImageOps.fit(building, SIZE, centering=(0.5, 0.5))

frames = []

for _ in range(3):  # ロゴ 1.5秒
    frames.append(logo)

for _ in range(6):  # 外観 3秒
    frames.append(building)

frames[0].save(
    "output.gif",
    save_all=True,
    append_images=frames[1:],
    duration=500,
    loop=0,
    optimize=True
)

print("GIF created: output.gif")
