import os
import string
import random

from django.utils.text import slugify


def generate_unique_slug(instance, new_slug=None) -> str:
    if new_slug is not None:
        slug = new_slug
    else: 
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{generate_random_string(size=4)}"
        return generate_unique_slug(instance, new_slug=new_slug)
    return slug


def get_upload_image_path(instance, filename: str, prefix: str,) -> str:
    new_filename = generate_random_string()
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"{prefix}/{final_filename}"


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(filename)
    return name, ext

def generate_random_string(size=10, chars=string.ascii_lowercase + string.digits) -> str:
    return "".join(random.choice(chars) for _ in range(size))
