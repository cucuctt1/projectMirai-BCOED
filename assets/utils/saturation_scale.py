import colorsys

def adjust_saturation(hex_color, scale_factor=1.0, down_val=None, brightness_factor=1.0):
    # Convert HEX to RGB
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    # Convert RGB to HLS (Hue, Lightness, Saturation)
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    # Adjust saturation based on conditions
    if down_val is not None:
        s = max(0, min(1, down_val))  # Force down_val into valid range (0-1)
    else:
        s *= scale_factor
        s = max(0, min(1, s))  # Ensure saturation remains in valid range

    # Adjust brightness (lightness)
    l *= brightness_factor
    l = max(0, min(1, l))  # Clamp lightness within valid range

    # Convert back to RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)

    # Format back to HEX
    return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
