from django.db import migrations

REGIONS = [
    "Tunis",
    "L'Ariana",
    "Beja",
    "Ben Arous",
    "Zaghouan",
    "Bizerte",
    "Jendouba",
    "Siliana",
    "Manouba",
    "Nabeul",
    "Kasserine",
    "Kairouan",
    "Sousse",
    "Gafsa",
    "Sidi Bouzid",
    "Medenine",
    "Tozeur",
    "Tataouine",
    "Kebili",
    "Gabes",
    "Monastir",
    "Sfax",
    "Mahdia",
]


def seed_regions(apps, schema_editor):
    Region = apps.get_model('complaints', 'Region')
    for name in REGIONS:
        Region.objects.get_or_create(name=name)


def remove_regions(apps, schema_editor):
    Region = apps.get_model('complaints', 'Region')
    Region.objects.filter(name__in=REGIONS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0002_region_complaint_city'),
    ]

    operations = [
        migrations.RunPython(seed_regions, remove_regions),
    ]
