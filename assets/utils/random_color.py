import random

def random_hex_color():
    return "#{:06X}".format(random.randint(0, 0xFFFFFF))