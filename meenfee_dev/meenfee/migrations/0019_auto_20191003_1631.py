# Generated by Django 2.2.1 on 2019-10-03 16:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meenfee', '0018_auto_20191003_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionfilledbyadmin',
            name='related_service_ids',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_end_time',
            field=models.TimeField(default='16:31:53'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_start_time',
            field=models.TimeField(default='16:31:53'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_end_time',
            field=models.TimeField(default='16:31:53'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_start_time',
            field=models.TimeField(default='16:31:53'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_end_time',
            field=models.TimeField(default='16:31:53'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_start_time',
            field=models.TimeField(default='16:31:53'),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 359996)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 359978)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360029)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360014)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360054)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360041)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361799)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361783)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361764)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361751)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361854)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361867)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361736)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361719)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 357865)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 357845)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 357893)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 357879)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 357919)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 357906)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_date',
            field=models.DateField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 355567)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_time',
            field=models.TimeField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 355593)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_date',
            field=models.DateField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 355379)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_time',
            field=models.TimeField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 355396)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_date',
            field=models.DateField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 355302)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_time',
            field=models.TimeField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 355321)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='created1',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 336790)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 336855)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360510)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360492)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360542)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360524)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360571)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 360555)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_date',
            field=models.DateField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 369777)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_time',
            field=models.TimeField(default=datetime.datetime(2019, 10, 3, 16, 31, 53, 369795)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='close_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 354554)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='open_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 354534)),
        ),
        migrations.AlterField(
            model_name='slots',
            name='end_time',
            field=models.TimeField(default='16:31:53'),
        ),
        migrations.AlterField(
            model_name='slots',
            name='start_time',
            field=models.TimeField(default='16:31:53'),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361023)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361004)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361051)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361037)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361077)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 361064)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 359469)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 359449)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 359502)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 359485)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 359534)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 359518)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358449)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358430)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358476)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358463)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358503)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358490)),
        ),
        migrations.AlterField(
            model_name='userotherinfo',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 348703), null=True),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358944)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358926)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358973)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358959)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358999)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 10, 3, 16, 31, 53, 358986)),
        ),
    ]
