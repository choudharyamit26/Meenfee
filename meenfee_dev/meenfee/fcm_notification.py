from pyfcm import FCMNotification
 
# push_service = FCMNotification(api_key="AAAAm_F88-w:APA91bFWWgclr8tpm7CHswqhAGI1sc0eL1O_sIn-0wxjVVtfh87U5AS3Xv_o_qiyE4kHeR0xZSyVKZvFBudbu0RxzqQXVFTmUJ8cbE3KH-uo6zvu7kHp6Gi9hHvqvLTnebOu4A9nOrBb")
push_service = FCMNotification(api_key="AAAAoSphLKQ:APA91bE9cqLQ25hRJxyQW7EL-5jS0-UeRm4wRfROqMIOZ_IFKSeFLq0tu8VKYFW0WD_xjdxFzO-Gfa8lCviNsVXoZpPJxaddc_R31yhy3SGCk-M0TPqBfkAWFzBlXQEZxVsz46VIHZAT")
 
# OR initialize with proxies
 
proxy_dict = {
          "http"  : "http://127.0.0.1"
        }
push_service = FCMNotification(api_key="AAAAoSphLKQ:APA91bE9cqLQ25hRJxyQW7EL-5jS0-UeRm4wRfROqMIOZ_IFKSeFLq0tu8VKYFW0WD_xjdxFzO-Gfa8lCviNsVXoZpPJxaddc_R31yhy3SGCk-M0TPqBfkAWFzBlXQEZxVsz46VIHZAT", proxy_dict=proxy_dict)
 
# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
 
def send_to_one(registration_id,message_title,message_body):
    # registration_id = "<device registration_id>"
    # message_title = "Uber update"
    # message_body = "Hi john, your customized news for today is ready"
    data_message = {"New Booking":"You have a new task added to your Jobs",}
    result = push_service.notify_single_device(registration_id, message_title,message_body,data_message)
    print("<----------------------------------------------------->",result)
 
# Send to multiple devices by passing a list of ids.
def send_to_many(registration_ids,message_title,message_body,result):
    registration_ids = ["<device registration_id 1>", "<device registration_id 2>"]
    message_title = "Uber update"
    message_body = "Hope you're having fun this weekend, don't forget to check today's news"
    # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
    print ("<---------------------------------------------------------->",result)
