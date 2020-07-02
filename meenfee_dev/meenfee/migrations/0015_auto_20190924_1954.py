# Generated by Django 2.2.1 on 2019-09-24 19:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meenfee', '0014_auto_20190924_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='settledpayments',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_end_time',
            field=models.TimeField(default='19:54:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_start_time',
            field=models.TimeField(default='19:54:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_end_time',
            field=models.TimeField(default='19:54:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_start_time',
            field=models.TimeField(default='19:54:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_end_time',
            field=models.TimeField(default='19:54:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_start_time',
            field=models.TimeField(default='19:54:50'),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405295)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405274)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405324)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405310)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405349)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405337)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406998)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406985)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406970)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406956)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 407053)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 407067)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406942)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406924)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403172)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403150)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403200)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403187)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403226)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403213)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 400946)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 400960)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 400811)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 400825)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 400740)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 400757)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='created1',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 382418)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 382482)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405814)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405794)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405842)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405828)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405868)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 405855)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 415155)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 24, 19, 54, 50, 415174)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='close_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 400084)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='open_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 400065)),
        ),
        migrations.AlterField(
            model_name='slots',
            name='end_time',
            field=models.TimeField(default='19:54:50'),
        ),
        migrations.AlterField(
            model_name='slots',
            name='start_time',
            field=models.TimeField(default='19:54:50'),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406324)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406305)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406352)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406338)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406377)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 406364)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404768)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404748)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404798)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404782)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404830)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404813)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403674)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403651)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403702)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403689)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403731)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 403716)),
        ),
        migrations.AlterField(
            model_name='userotherinfo',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 394096), null=True),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404183)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404164)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404211)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404197)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404240)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 19, 54, 50, 404224)),
        ),
    ]
