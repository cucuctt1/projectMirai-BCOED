import random
import string

def random_string(n=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))