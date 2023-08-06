[![](https://img.shields.io/badge/released-2021.6.4-green.svg?longCache=True)](https://pypi.org/project/django-bulk/)
[![](https://img.shields.io/badge/license-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)

### Installation
```bash
$ pip install django-bulk
```

### Pros
+   reduces the amount of code when you need a lot of `bulk_create`, `bulk_update`, `delete` operations

### How it works
1.  add objects `django_bulk.create(obj)`, `django_bulk.update(obj,**kwargs)`, `django_bulk.delete(obj)`
2.  run `django_bulk.execute()`

### Examples
```python
import django_bulk

from my_apps.models import MyModel

# create
django_bulk.create(MyModel(key="value1"))
django_bulk.create(MyModel(key="value2"))

# update
django_bulk.update(obj1,key="value1")
django_bulk.update(obj2,key="value2")

# delete
for obj in queryset:
    django_bulk.delete(obj)

django_bulk.execute()
```

