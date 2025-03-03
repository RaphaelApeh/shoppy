from django.utils.text import slugify


def generate_unique_slug(instance, **kwargs):
    
    Klass = instance.__class__
    slug_field = kwargs.setdefault("slug_field", "slug")
    slug = slugify(instance.name)
    count = 0

    while Klass.objects.filter(**{slug_field: slug}).exists():
        slug = slugify("%s-%d" % (instance.name, count))
        count += 1
    return slug