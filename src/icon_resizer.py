# 3
from PIL import Image
import os

# 3
def resize_icon(source_path, output_dir, sizes):
    """
    Redimensiona o ícone para múltiplos tamanhos e salva na pasta de assets.
    """
    # 3
    if not os.path.exists(output_dir):
        # 3
        os.makedirs(output_dir)

    # 3
    img = Image.open(source_path).convert("RGBA")
    
    # 3
    for size in sizes:
        # 3
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        # 3
        # Salva com o nome padronizado icon_larguraxaltura.png
        output_path = os.path.join(output_dir, f"icon_{size}x{size}.png")
        # 3
        resized.save(output_path, "PNG")
        # 3
        print(f"Ícone salvo em {output_path}")

# 3
if __name__ == "__main__":
    # 3
    # Caminho relativo para funcionar de qualquer lugar do projeto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 3
    source_icon = os.path.join(base_dir, "assets", "icon.png")
    # 3
    assets_dir = os.path.join(base_dir, "assets")
    # 3
    icon_sizes = [16, 32, 64, 128, 256]
    
    # 3
    if os.path.exists(source_icon):
        # 3
        resize_icon(source_icon, assets_dir, icon_sizes)
    else:
        # 3
        print(f"Erro: Ícone original não encontrado em '{source_icon}'.")
