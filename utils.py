import random

random_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def generate_random_code(length):
    return ''.join(random.choice(random_characters) for _ in range(length))