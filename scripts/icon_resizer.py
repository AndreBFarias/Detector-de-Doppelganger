from __future__ import annotations

import os

from PIL import Image, ImageFilter


def create_icon_with_black_glow(source_img: Image.Image, target_size: int) -> Image.Image:
    """
    Creates an icon of target_size with the source image scaled down
    and a black glow/shadow applied behind it. Trim transparent borders first.
    """
    # 1. Trim transparent borders (Auto-Crop)
    bbox = source_img.getbbox()
    if bbox:
        trimmed_img = source_img.crop(bbox)
    else:
        trimmed_img = source_img

    # 2. Determine inner size target
    # Reduce padding to 5% to maximize size
    padding_factor = 0.05
    max_dim = int(target_size * (1 - 2 * padding_factor))
    if max_dim < 1:
        max_dim = 1

    # Calculate resize maintaining aspect ratio
    width, height = trimmed_img.size
    ratio = min(max_dim / width, max_dim / height)
    new_size = (int(width * ratio), int(height * ratio))

    # Resize source image (High Quality)
    img_inner = trimmed_img.resize(new_size, Image.Resampling.LANCZOS)

    # 3. Create the Shadow/Glow
    # Create a canvas for the shadow
    shadow_canvas = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))

    # Extract alpha from inner image to use as mask for shadow
    r, g, b, alpha = img_inner.split()

    # Create solid black image of inner size
    black_shape = Image.new("RGBA", new_size, (0, 0, 0, 255))
    black_shape.putalpha(alpha)

    # Calculate centered position
    offset_x = (target_size - new_size[0]) // 2
    offset_y = (target_size - new_size[1]) // 2

    shadow_canvas.paste(black_shape, (offset_x, offset_y), mask=black_shape)

    # Determine blur radius based on target size
    if target_size >= 512:
        radius = 8
    elif target_size >= 256:
        radius = 6
    elif target_size >= 128:
        radius = 4
    elif target_size >= 64:
        radius = 3
    elif target_size >= 48:
        radius = 2
    elif target_size >= 32:
        radius = 1.5
    else:
        radius = 1

    # Apply Gaussian Blur to create the glow
    shadow = shadow_canvas.filter(ImageFilter.GaussianBlur(radius))

    # 4. Composite
    # Create final canvas
    final_icon = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))

    # Paste shadow first
    final_icon.alpha_composite(shadow)

    # Paste the colored inner icon on top
    # Use alpha_composite for better blending if resizing introduced semi-transparency
    img_layer = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
    img_layer.paste(img_inner, (offset_x, offset_y))
    final_icon = Image.alpha_composite(final_icon, img_layer)

    return final_icon


def resize_icon(source_path: str, output_dir: str, sizes: list[int]) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        source_img = Image.open(source_path).convert("RGBA")

        for size in sizes:
            # Generate styled icon
            processed = create_icon_with_black_glow(source_img, size)

            output_path = os.path.join(output_dir, f"icon_{size}x{size}.png")
            processed.save(output_path, "PNG")
            print(f"Ícone salvo em {output_path}")

    except Exception as e:
        print(f"Erro ao processar ícones: {e}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_icon = os.path.join(base_dir, "assets", "icon.png")
    assets_dir = os.path.join(base_dir, "assets")
    icon_sizes = [16, 32, 48, 64, 128, 256, 512]

    if os.path.exists(source_icon):
        resize_icon(source_icon, assets_dir, icon_sizes)
    else:
        print(f"Erro: Ícone original não encontrado em '{source_icon}'.")

# "A simplicidade e o ultimo grau de sofisticacao." - Leonardo da Vinci
