from django_cron import CronJobBase, Schedule
from django_cron.models import *
from meenfee.models import *
from django.db.models import Q,F
from django.utils import timezone
from meenfee.fcm_notification import send_to_one,send_to_many

PROVIDER_STRING = "provider"
REQUESTOR_STRING = "requester"
TIME_LIMIT = "3"

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'

    def do(self):
        # pass
        current_time = timezone.now()
        
        BookingQS = NewBookings.objects. \
        filter(Q(accepted_by_provider = False) | Q(accepted_by_requester = False)). \
        exclude(Q(booking_cancelled = True)|Q(booking_completed = True)). \
        filter(auto_cancellation_time__lte=current_time)

        last_cron_time = current_time - timedelta(minutes=60)
        CronQS = CronJobLog.objects.filter(start_time__lte = last_cron_time).delete()

        for obj in BookingQS:

            try:
                LivePaymentObject = LivePayments.objects.get(booking_ID__exact=obj.booking_id)
                obj.auto_cancelled          = True
                obj.booking_cancelled       = True
                obj.booking_closure_time    = current_time
                obj.save()

                fcm_provider    =   obj.provider_id.fcm_token
                fcm_requester   =   obj.requestor_id.fcm_token

                message_body_requester = "No action was performed on this booking in the last " + TIME_LIMIT + " hours neither by the you or the service provider and hence has been cancelled.Kindly make a new booking request."
                message_body_provider = "No action was performed on this booking in the last " + TIME_LIMIT + " hours neither by the you or the service requester and hence has been cancelled."

                try:
                    send_to_one(fcm_provider,message_body_provider,"Booking cancelled due to inactivity.")
                    send_to_one(fcm_requester,message_body_requester,"Booking cancelled due to inactivity.")
                except:
                    pass


                InAppBookingNotificationsObject_Requester = InAppBookingNotifications(
                    from_user_id            = obj.provider_id,
                    from_user_name          = obj.provider_id.user.get_full_name(),
                    to_user_id              = obj.requestor_id,
                    to_user_name            = obj.requestor_id.user.get_full_name(),
                    notification_type       = "Booking Cancelled",
                    notification_title      = message_body_requester,
                    service_name            = obj.service_name,
                    requested_service_time  = obj.service_time,
                    requested_service_date  = obj.service_date,
                    notification_time       = timezone.now(),
                    notification_date       = timezone.now(),
                    service_pricing         = obj.service_charges,
                    service_place           = "At Provider's Place",
                    to_user_usertype        = REQUESTOR_STRING,
                    )
                
                InAppBookingNotificationsObject_Requester.save()

                InAppBookingNotificationsObject_Provider = InAppBookingNotifications(
                    from_user_id            = obj.requestor_id,
                    from_user_name          = obj.requestor_id.user.get_full_name(),
                    to_user_id              = obj.provider_id,
                    to_user_name            = obj.provider_id.user.get_full_name(),
                    notification_type       = "Booking Cancelled",
                    notification_title      = message_body_provider,
                    service_name            = obj.service_name,
                    requested_service_time  = obj.service_time,
                    requested_service_date  = obj.service_date,
                    notification_time       = timezone.now(),
                    notification_date       = timezone.now(),
                    service_pricing         = obj.service_charges,
                    service_place           = "At Provider's Place",
                    to_user_usertype        = PROVIDER_STRING,
                    )
                
                InAppBookingNotificationsObject_Provider.save()

                LivePaymentObject.delete()
            except:
                pass