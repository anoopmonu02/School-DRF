from django.utils.text import slugify
import uuid


def generate_slug(title:str, obj, slug_field='slug')->str:

    """ A function to generate a slug """
    title = slugify(title)    
    ourObj = obj.__class__
    
    while ourObj.objects.filter(**{slug_field:title}).exists():
        title = f'{slugify(title)}-{str(uuid.uuid4())[:4]}'

    return title

