import collections
from django.db import transaction

bulk_create_objs = collections.defaultdict(list)
bulk_delete_objs = collections.defaultdict(list)
bulk_update_objs = collections.defaultdict(list)
bulk_update_fields = collections.defaultdict(list)

def create(obj):
    bulk_create_objs[obj.__class__].append(obj)

def delete(obj):
    bulk_delete_objs[obj.__class__].append(obj)

def update(obj, **kwargs):
    bulk_update_fields[obj.__class__] = list(kwargs.keys())
    new_kwargs = {k: v for k, v in kwargs.items() if hasattr(
        obj, k) and getattr(obj, k) != v}
    if new_kwargs:
        for k, v in new_kwargs.items():
            setattr(obj, k, v)
        bulk_update_objs[obj.__class__].append(obj)
    return new_kwargs

def bulk_create():
    for model, objs in bulk_create_objs.items():
        model.objects.bulk_create(objs)
    bulk_create_objs.clear()

def bulk_delete():
    for model, objs in bulk_delete_objs.items():
        delete_ids = list(map(lambda obj: obj.id, objs))
        model.objects.filter(id__in=delete_ids).delete()
    bulk_delete_objs.clear()

def bulk_update():
    for model, objs in bulk_update_objs.items():
        update_fields = bulk_update_fields[model]
        model.objects.bulk_update(objs, update_fields)
    bulk_update_fields.clear()
    bulk_update_objs.clear()

def execute():
    if bulk_create_objs or bulk_delete_objs or bulk_update_objs:
        with transaction.atomic():
            bulk_create()
            bulk_update()
            bulk_delete()
