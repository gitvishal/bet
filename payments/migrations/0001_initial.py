# Generated by Django 2.2 on 2020-02-13 08:35

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import jsonfield.fields
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=45, unique=True)),
                ('amount', django_cryptography.fields.encrypt(models.DecimalField(decimal_places=2, max_digits=10))),
                ('reason', django_cryptography.fields.encrypt(ckeditor.fields.RichTextField())),
                ('meta_data', django_cryptography.fields.encrypt(jsonfield.fields.JSONField(blank=True, null=True))),
                ('confirmed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('inprocess', 'in process'), ('success', 'success'), ('failed', 'failed')], max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalTransaction',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address')),
                ('transaction_id', models.CharField(db_index=True, max_length=45)),
                ('amount', django_cryptography.fields.encrypt(models.DecimalField(decimal_places=2, max_digits=10))),
                ('reason', django_cryptography.fields.encrypt(ckeditor.fields.RichTextField())),
                ('meta_data', django_cryptography.fields.encrypt(jsonfield.fields.JSONField(blank=True, null=True))),
                ('confirmed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('inprocess', 'in process'), ('success', 'success'), ('failed', 'failed')], max_length=45)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical transaction',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOnlinePlayerBalanceAccount',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address')),
                ('transaction_type', models.CharField(choices=[('credit', 'credit'), ('debit', 'debit')], max_length=45)),
                ('created_on', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('player', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='master.OnlinePlayer')),
                ('transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='payments.Transaction')),
            ],
            options={
                'verbose_name': 'historical online player balance account',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAgentBalanceAccount',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address')),
                ('transaction_type', models.CharField(choices=[('credit', 'credit'), ('debit', 'debit')], max_length=45)),
                ('created_on', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('agent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='master.Agent')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='payments.Transaction')),
            ],
            options={
                'verbose_name': 'historical agent balance account',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='OnlinePlayerBalanceAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('credit', 'credit'), ('debit', 'debit')], max_length=45)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='onlineplayerbalanceaccount_online_player', to='master.OnlinePlayer')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='onlineplayerbalanceaccount_trans', to='payments.Transaction')),
            ],
            options={
                'unique_together': {('player', 'transaction')},
            },
        ),
        migrations.CreateModel(
            name='AgentBalanceAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('credit', 'credit'), ('debit', 'debit')], max_length=45)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agentbalanceaccount_agent', to='master.Agent')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='agentbalanceaccount_trans', to='payments.Transaction')),
            ],
            options={
                'unique_together': {('agent', 'transaction')},
            },
        ),
    ]
