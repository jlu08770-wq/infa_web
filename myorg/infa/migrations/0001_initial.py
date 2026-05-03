from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='InfaUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('model', 'Model'), ('organizer', 'Organizer'), ('admin', 'Admin')], max_length=20)),
                ('verified', models.BooleanField(default=False)),
                ('location', models.CharField(blank=True, max_length=120)),
                ('bio', models.TextField(blank=True)),
                ('avatar_url', models.URLField(blank=True)),
                ('cover_image_url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InfaModelProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=50)),
                ('experience', models.TextField()),
                ('height_cm', models.PositiveIntegerField(blank=True, null=True)),
                ('portfolio_image_url', models.URLField(blank=True)),
                ('instagram_handle', models.CharField(blank=True, max_length=80)),
                ('featured', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, to='infa.infauser')),
            ],
        ),
        migrations.CreateModel(
            name='InfaOpportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('paid', 'Paid'), ('collaboration', 'Collaboration')], max_length=20)),
                ('budget', models.IntegerField()),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=20)),
                ('category', models.CharField(blank=True, max_length=50)),
                ('location', models.CharField(blank=True, max_length=120)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('image_url', models.URLField(blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('organizer', models.ForeignKey(limit_choices_to={'role': 'organizer'}, on_delete=models.deletion.CASCADE, to='infa.infauser')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_date', models.DateTimeField(auto_now_add=True)),
                ('model', models.ForeignKey(limit_choices_to={'role': 'model'}, on_delete=models.deletion.CASCADE, related_name='model_visits', to='infa.infauser')),
                ('organizer', models.ForeignKey(limit_choices_to={'role': 'organizer'}, on_delete=models.deletion.CASCADE, related_name='organizer_visits', to='infa.infauser')),
            ],
        ),
        migrations.CreateModel(
            name='OpportunityApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('under_review', 'Under Review'), ('hired', 'Hired'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='applied', max_length=20)),
                ('cover_note', models.TextField(blank=True)),
                ('applied_on', models.DateField(auto_now_add=True)),
                ('model_profile', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='applications', to='infa.infamodelprofile')),
                ('opportunity', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='applications', to='infa.infaopportunity')),
            ],
            options={
                'unique_together': {('opportunity', 'model_profile')},
            },
        ),
    ]
