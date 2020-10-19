# Generated by Django 2.2 on 2020-10-19 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_question_text', models.CharField(max_length=200)),
                ('g_pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_choice_text', models.CharField(max_length=200)),
                ('g_votes', models.IntegerField(default=0)),
                ('g_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
            ],
        ),
    ]