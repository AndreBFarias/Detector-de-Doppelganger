def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def interpolate_color(start_hex, end_hex, factor):
    """
    Interpolates between two hex colors.
    factor: 0.0 to 1.0
    """
    c1 = hex_to_rgb(start_hex)
    c2 = hex_to_rgb(end_hex)

    r = int(c1[0] + (c2[0] - c1[0]) * factor)
    g = int(c1[1] + (c2[1] - c1[1]) * factor)
    b = int(c1[2] + (c2[2] - c1[2]) * factor)

    return rgb_to_hex((r, g, b))


def get_color_for_percentage(percentage, inverse=False):
    """
    Returns a color between Green and Red based on percentage (0.0 to 1.0).
    inverse=False (Naturalness): 0% -> Red, 100% -> Green
    inverse=True (Similarity): 0% -> Green, 100% -> Red
    """
    # Cores Dracula Theme adaptadas
    GREEN = "#50FA7B"
    RED = "#FF5555"

    # Se quiser "Vinho", podemos usar um vermelho mais escuro/intenso, mas #FF5555 é bom para dark mode.
    # Vamos tentar um vermelho mais "vinho" se solicitado, mas legibilidade é chave.
    # Vou usar #FF5555 por enquanto.

    if inverse:
        # Similarity: 0% Green -> 100% Red
        return interpolate_color(GREEN, RED, percentage)
    else:
        # Naturalness: 0% Red -> 100% Green
        return interpolate_color(RED, GREEN, percentage)
