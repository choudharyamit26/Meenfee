# Generated by Django 2.2.1 on 2019-09-19 14:59

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meenfee', '0002_auto_20190919_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_end_time',
            field=models.TimeField(default='14:59:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_1_start_time',
            field=models.TimeField(default='14:59:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_end_time',
            field=models.TimeField(default='14:59:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_2_start_time',
            field=models.TimeField(default='14:59:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_end_time',
            field=models.TimeField(default='14:59:50'),
        ),
        migrations.AlterField(
            model_name='dayandslots',
            name='slot_3_start_time',
            field=models.TimeField(default='14:59:50'),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237636)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237617)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237663)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237650)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237689)),
        ),
        migrations.AlterField(
            model_name='friday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237676)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 239340)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='notification_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 239327)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 239314)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='requested_service_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 239300)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 239394)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='rescheduled_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 239408)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 239286)),
        ),
        migrations.AlterField(
            model_name='inappbookingnotifications',
            name='service_slot_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 239266)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 235448)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 235428)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 235492)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 235462)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 235519)),
        ),
        migrations.AlterField(
            model_name='monday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 235506)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 233373)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='cancellation_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 233389)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 233236)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='rescheduled_service_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 233250)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 233165)),
        ),
        migrations.AlterField(
            model_name='newbookings',
            name='service_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 233183)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='created1',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 214524)),
        ),
        migrations.AlterField(
            model_name='providersrating',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 214587)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238153)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238135)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238181)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238167)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238206)),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238194)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 247303)),
        ),
        migrations.AlterField(
            model_name='servicefeedback',
            name='feedback_time',
            field=models.TimeField(default=datetime.datetime(2019, 9, 19, 14, 59, 50, 247331)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='close_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 232510)),
        ),
        migrations.AlterField(
            model_name='serviceschedule',
            name='open_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 232490)),
        ),
        migrations.AlterField(
            model_name='slots',
            name='end_time',
            field=models.TimeField(default='14:59:50'),
        ),
        migrations.AlterField(
            model_name='slots',
            name='start_time',
            field=models.TimeField(default='14:59:50'),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238667)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238649)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238695)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238682)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238721)),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 238708)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237078)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237059)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237109)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237092)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237135)),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 237122)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 235977)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 235958)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 236005)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 235991)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 236031)),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 236018)),
        ),
        migrations.AlterField(
            model_name='userotherinfo',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 226422), null=True),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 236488)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot1_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 236469)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 236519)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot2_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 236502)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_end',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 236622)),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='slot3_start',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 19, 14, 59, 50, 236606)),
        ),
        migrations.CreateModel(
            name='SettledPaymentsRefund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('Card', 'Card'), ('Cash', 'Cash')], max_length=30)),
                ('payment_request_date', models.DateField(default=django.utils.timezone.now)),
                ('payment_request_time', models.TimeField(default=django.utils.timezone.now)),
                ('payment_settle_date', models.DateField(default=django.utils.timezone.now)),
                ('payment_settle_time', models.TimeField(default=django.utils.timezone.now)),
                ('booking_ID', models.CharField(blank=True, max_length=70, null=True)),
                ('cash_paid_by_requestor', models.BooleanField(default=False)),
                ('cash_collected_by_provider', models.BooleanField(default=False)),
                ('admin_charges', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('service_charges', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total_amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('transaction_type', models.CharField(blank=True, default='', max_length=80, null=True)),
                ('gateway_merchant_id', models.CharField(blank=True, default='', max_length=80, null=True)),
                ('gateway_transaction_id', models.CharField(blank=True, default='', max_length=80, null=True)),
                ('payment_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Settled_Payments_Refund_Refund', to='meenfee.BankingInfo')),
                ('payment_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Settled_Payments_Refund_From', to='meenfee.UserOtherInfo')),
                ('payment_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Settled_Payments_Refund_To', to='meenfee.UserOtherInfo')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Settled_Payments_Refund_Service', to='meenfee.Service')),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Settled_Payments_Refund_Transaction', to='meenfee.CardTransactionMaster')),
            ],
        ),
        migrations.CreateModel(
            name='SettledPaymentsCancel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('Card', 'Card'), ('Cash', 'Cash')], max_length=30)),
                ('payment_request_date', models.DateField(default=django.utils.timezone.now)),
                ('payment_request_time', models.TimeField(default=django.utils.timezone.now)),
                ('payment_settle_date', models.DateField(default=django.utils.timezone.now)),
                ('payment_settle_time', models.TimeField(default=django.utils.timezone.now)),
                ('booking_ID', models.CharField(blank=True, max_length=70, null=True)),
                ('cash_paid_by_requestor', models.BooleanField(default=False)),
                ('cash_collected_by_provider', models.BooleanField(default=False)),
                ('admin_charges', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('service_charges', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total_amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('transaction_type', models.CharField(blank=True, default='', max_length=80, null=True)),
                ('gateway_merchant_id', models.CharField(blank=True, default='', max_length=80, null=True)),
                ('gateway_transaction_id', models.CharField(blank=True, default='', max_length=80, null=True)),
                ('payment_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Settled_PaymentsCancel', to='meenfee.BankingInfo')),
                ('payment_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Settled_Payments_Cancel_From', to='meenfee.UserOtherInfo')),
                ('payment_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Settled_Payments_Cancel_To', to='meenfee.UserOtherInfo')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Settled_PaymentsCancel', to='meenfee.Service')),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Settled_Payments_Cancel_transaction', to='meenfee.CardTransactionMaster')),
            ],
        ),
    ]
