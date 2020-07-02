from rest_framework.views 			import APIView
from rest_framework.response 		import Response
from rest_framework.status 			import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework_jwt.settings 	import api_settings
from django.utils                   import timezone
from django.contrib.auth 			import get_user_model
from app.models                     import UserOtherInfo

jwt_payload_handler     = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler      = api_settings.JWT_ENCODE_HANDLER


class UserLogin(APIView):
    '''
    API to login Users.
    On successful login in, a token is returned in response and will be used
    by the user to make authenticated requests henceforth.

    '''

    def post(self,request):

		user_data ={
			"username" 			: "",
			"first_name" 		: "",
			"last_name" 		: "",
			"email" 			: "",
			"phone" 			: "",
			"user_address" 		: "",
			"user_address_lat" 	: "",
			"user_address_long" : "",
			"profile_image" 	: "",
			"idcard" 			: "",
			"bio" 				: "",
			"token" 			: "",
			"social_login"		: False,
			"usertype"			: "",
			}

		login_time          = timezone.now()
		incoming_data       = request.data
		usertype            = incoming_data['usertype']
		current_language    = incoming_data['current_language']
		email_raw           = incoming_data['email']
		password            = incoming_data['password']
		
		email               = email_raw.lower()
		data                = {}
		try:
			user_object     = User.objects.get(email=email)
			check_pass      = user_object.check_password(password)

			if check_pass == True:
				payload     = jwt_payload_handler(user_object)
				token       = jwt_encode_handler(payload)
				uoi_object  = UserOtherInfo.objects.get(user=user_object)

				if uoi_object.usertype == usertype:
					uoi_object.usertype             = usertype
					uoi_object.current_language     =  current_language
					uoi_object.save()
					user_data['username']           = user_object.username
					user_data['first_name']         = user_object.first_name
					user_data['last_name']          = user_object.last_name
					user_data['email']              = user_object.email
					user_data['phone']              = uoi_object.phone
					user_data['user_address']       = uoi_object.user_address
					user_data['user_address_lat']   = uoi_object.user_address_lat
					user_data['user_address_long']  = uoi_object.user_address_long
					user_data['profile_image']      = uoi_object.profile_image_s3
					user_data['usertype']           = uoi_object.usertype
					
					if uoi_object.idcard  in [None,""]:
						user_data['idcard'] = ""
					else:
						user_data['idcard'] = uoi_object.idcard
						
					if uoi_object.bio in [None,""]:
						user_data['bio']    = ""
					else:
						user_data['bio']    = uoi_object.bio

					data['token']           = token
					data['data']            = user_data
					user_object.last_login  = login_time
					user_object.save()
					return Response(data,status=HTTP_200_OK)
				else:
					if uoi_object.usertype == "Provider" or uoi_object.usertype == "provider":
						return Response({"msg":"You were previously logged in as Provider.Please log in to change your usertype.","status":"LAST_SESSION_PROVIDER"},status=HTTP_400_BAD_REQUEST)
					else:
						return Response({"msg":"You were previously logged in as Requestor.Please log in to change your usertype.","status":"LAST_SESSION_REQUESTOR"},status=HTTP_400_BAD_REQUEST)
			else:
				return Response({"msg":"Wrong Password"},status=HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({"msg":"User with this email ID does not exist"},status=HTTP_400_BAD_REQUEST)

	