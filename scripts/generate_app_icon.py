from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


def _rounded_rectangle(draw: ImageDraw.ImageDraw, xy, radius: int, fill):
    # Pillow has rounded_rectangle in newer versions, but keep it explicit.
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def generate_calculator_icon_png(size: int) -> Image.Image:
    """Generates a simple calculator icon (original artwork) as RGBA PNG."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    pad = max(1, size // 18)
    body_radius = max(6, size // 10)

    # Outer body
    _rounded_rectangle(
        d,
        (pad, pad, size - pad, size - pad),
        radius=body_radius,
        fill=(20, 22, 28, 255),
    )

    # Inner inset
    inset = pad + max(2, size // 60)
    _rounded_rectangle(
        d,
        (inset, inset, size - inset, size - inset),
        radius=max(5, body_radius - max(2, size // 40)),
        fill=(28, 31, 40, 255),
    )

    # Display area
    display_h = int(size * 0.23)
    display_pad_x = int(size * 0.10)
    display_top = int(size * 0.12)
    display_bottom = display_top + display_h

    _rounded_rectangle(
        d,
        (display_pad_x, display_top, size - display_pad_x, display_bottom),
        radius=max(6, size // 30),
        fill=(18, 80, 60, 255),
    )

    # Display shine
    d.rectangle(
        (
            display_pad_x + int(size * 0.03),
            display_top + int(size * 0.03),
            size - display_pad_x - int(size * 0.03),
            display_top + int(size * 0.06),
        ),
        fill=(255, 255, 255, 30),
    )

    # Buttons grid (3x4) + right column operators
    grid_top = int(size * 0.40)
    grid_left = int(size * 0.12)
    grid_right = int(size * 0.88)
    grid_bottom = int(size * 0.88)

    cols = 4
    rows = 4
    gap = int(size * 0.03)
    bw = int((grid_right - grid_left - gap * (cols - 1)) / cols)
    bh = int((grid_bottom - grid_top - gap * (rows - 1)) / rows)

    def button_rect(c: int, r: int):
        x0 = grid_left + c * (bw + gap)
        y0 = grid_top + r * (bh + gap)
        return (x0, y0, x0 + bw, y0 + bh)

    btn_radius = max(5, size // 35)

    # Colors
    num_fill = (50, 54, 66, 255)
    op_fill = (230, 145, 36, 255)
    fun_fill = (60, 65, 80, 255)

    # Top row: C, ±, %, ÷
    for c in range(3):
        _rounded_rectangle(d, button_rect(c, 0), radius=btn_radius, fill=fun_fill)
    _rounded_rectangle(d, button_rect(3, 0), radius=btn_radius, fill=op_fill)

    # Middle rows: numbers + operators
    for r in range(1, 4):
        for c in range(3):
            _rounded_rectangle(d, button_rect(c, r), radius=btn_radius, fill=num_fill)
        _rounded_rectangle(d, button_rect(3, r), radius=btn_radius, fill=op_fill)

    # Subtle highlights
    highlight = (255, 255, 255, 18)
    for r in range(0, 4):
        for c in range(0, 4):
            x0, y0, x1, y1 = button_rect(c, r)
            d.rectangle((x0 + 2, y0 + 2, x1 - 2, y0 + 6), fill=highlight)

    return img


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    assets_dir = project_root / "assets"
    installer_dir = project_root / "installer"

    assets_dir.mkdir(parents=True, exist_ok=True)
    installer_dir.mkdir(parents=True, exist_ok=True)

    png_path = assets_dir / "app.png"
    ico_path = assets_dir / "app.ico"
    installer_ico_path = installer_dir / "app.ico"

    img_512 = generate_calculator_icon_png(512)
    img_512.save(png_path, format="PNG")

    # ICO with multiple sizes for best results in Windows.
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img_512.save(ico_path, format="ICO", sizes=sizes)

    # Reuse same icon for installer.
    installer_ico_path.write_bytes(ico_path.read_bytes())

    print(f"OK: gerado {png_path}")
    print(f"OK: gerado {ico_path}")
    print(f"OK: copiado {installer_ico_path}")


if __name__ == "__main__":
    main()
