import skia


def measure_text_skia(text, font_size=16):
    font = skia.Font(skia.Typeface('Arial'), font_size)
    paint = skia.Paint()

    # Create a Rect object to store the text bounds
    bounds = skia.Rect()

    # Measure text width correctly
    width = font.measureText(text, skia.TextEncoding.kUTF8, bounds, paint)

    # Extract width and height from the bounds
    text_width = bounds.width()
    text_height = bounds.height()


    return text_width, text_height-10