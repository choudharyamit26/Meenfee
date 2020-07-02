# Generated by Django 2.2.1 on 2019-10-11 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meenfee', '0026_auto_20191010_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardtransactionmaster',
            name='raw_json_response_string',
            field=models.CharField(blank=True, default='', max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_end_time',
            field=models.TimeField(default='12:39:18'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_start_time',
            field=models.TimeField(default='12:39:18'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_end_time',
            field=models.TimeField(default='12:39:18'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_start_time',
            field=models.TimeField(default='12:39:18'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_end_time',
            field=models.TimeField(default='12:39:18'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_start_time',
            field=models.TimeField(default='12:39:18'),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716772)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716754)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716800)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716787)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716831)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716813)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 718451)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 718438)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 718425)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 718411)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 718504)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 718518)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 718392)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 718375)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 714596)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 714577)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 714624)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 714610)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 714654)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 714641)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_date',
            field=models.DateField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 712337)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_time',
            field=models.TimeField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 712353)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_date',
            field=models.DateField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 712204)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_time',
            field=models.TimeField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 712217)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_date',
            field=models.DateField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 712137)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_time',
            field=models.TimeField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 712155)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='created1',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 693108)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 693173)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717286)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717267)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717314)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717300)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717340)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717327)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_date',
            field=models.DateField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 726637)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_time',
            field=models.TimeField(default=datetime.datetime(2019, 10, 11, 12, 39, 18, 726657)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='close_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 711455)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='open_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 711432)),
        ),
        migrations.AlterField(
            model_name='slots',
            name='end_time',
            field=models.TimeField(default='12:39:18'),
        ),
        migrations.AlterField(
            model_name='slots',
            name='start_time',
            field=models.TimeField(default='12:39:18'),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717788)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717769)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717816)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717802)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717845)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 717832)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716263)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716244)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716291)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716277)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716321)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 716308)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715109)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715090)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715139)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715123)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715165)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715152)),
        ),
        migrations.AlterField(
            model_name='userotherinfo',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 705392), null=True),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715683)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715663)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715711)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715697)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715742)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 11, 12, 39, 18, 715724)),
        ),
    ]
