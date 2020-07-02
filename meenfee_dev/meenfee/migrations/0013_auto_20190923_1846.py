# Generated by Django 2.2.1 on 2019-09-23 18:46

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meenfee', '0012_auto_20190923_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='newbookings',
            name='booking_closure_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_end_time',
            field=models.TimeField(default='18:46:40'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_start_time',
            field=models.TimeField(default='18:46:40'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_end_time',
            field=models.TimeField(default='18:46:40'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_start_time',
            field=models.TimeField(default='18:46:40'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_end_time',
            field=models.TimeField(default='18:46:40'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_start_time',
            field=models.TimeField(default='18:46:40'),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813326)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813307)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813358)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813341)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813385)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813372)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 815158)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 815079)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 815064)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 815050)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 815218)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 815233)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 815035)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 815018)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811006)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 810986)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811040)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811023)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811075)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811056)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 808831)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 808845)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 808690)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 808705)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 808621)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 808638)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='created1',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 790474)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 790538)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813902)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813882)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813930)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813916)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813957)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 813944)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 823197)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 23, 18, 46, 40, 823217)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='close_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 807973)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='open_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 807952)),
        ),
        migrations.AlterField(
            model_name='slots',
            name='end_time',
            field=models.TimeField(default='18:46:40'),
        ),
        migrations.AlterField(
            model_name='slots',
            name='start_time',
            field=models.TimeField(default='18:46:40'),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 814417)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 814398)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 814446)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 814432)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 814472)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 814459)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812806)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812784)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812838)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812820)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812865)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812852)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811593)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811574)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811625)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811608)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811653)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 811640)),
        ),
        migrations.AlterField(
            model_name='userotherinfo',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 802042), null=True),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812189)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812168)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812222)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812206)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812259)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 23, 18, 46, 40, 812243)),
        ),
    ]
