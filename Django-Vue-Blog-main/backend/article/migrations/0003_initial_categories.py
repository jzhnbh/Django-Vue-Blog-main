from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('article', 'Category')
    categories = [
        {
            'name': '论文',
            'description': '有主见、有议程的长篇叙事写作'
        },
        {
            'name': '手账',
            'description': '对于我还不完全理解的事情，做出松散且不带任何偏见的记录'
        },
        {
            'name': '技术',
            'description': '从我自己的观察和研究中收集的设计模式'
        },
        {
            'name': '花园',
            'description': '数字花园是随着时间的推移慢慢生长的不完美的笔记'
        }
    ]
    
    for category in categories:
        Category.objects.create(**category)

def reverse_initial_categories(apps, schema_editor):
    Category = apps.get_model('article', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('article', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_initial_categories,
            reverse_initial_categories
        )
    ] 