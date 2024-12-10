# Generated by Django 5.1.4 on 2024-12-10 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_category_category_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapati',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapati_name', models.CharField(max_length=200)),
                ('chapati_description', models.Field(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('image', models.ImageField(blank=True, null=True, upload_to='chapati_images/')),
            ],
        ),
        migrations.AddField(
            model_name='regularpizza',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pizza_images/'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_description',
            field=models.Field(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='regularpizza',
            name='category_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sicilianpizza',
            name='category_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
