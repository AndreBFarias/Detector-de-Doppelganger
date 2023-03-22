from __future__ import annotations

import os

from PIL import Image


def resize_icon(source_path: str, output_dir: str, sizes: list[int]) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = Image.open(source_path).convert("RGBA")

    for size in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        output_path = os.path.join(output_dir, f"icon_{size}x{size}.png")
        resized.save(output_path, "PNG")
        print(f"Ícone salvo em {output_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_icon = os.path.join(base_dir, "assets", "icon.png")
    assets_dir = os.path.join(base_dir, "assets")
    icon_sizes = [16, 32, 64, 128, 256]

    if os.path.exists(source_icon):
        resize_icon(source_icon, assets_dir, icon_sizes)
    else:
        print(f"Erro: Ícone original não encontrado em '{source_icon}'.")


# "A arte de simplificar e a arte de eliminar o desnecessario." - Hans Hofmann
