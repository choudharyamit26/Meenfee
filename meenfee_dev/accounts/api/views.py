from rest_framework.generics 		import (CreateAPIView,)

from rest_framework_jwt.settings 	import api_settings

from rest_framework.views 			import APIView
from rest_framework.response 		import Response
from rest_framework.status 			import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT,HTTP_201_CREATED

from django.contrib.auth 			import get_user_model
from rest_framework.permissions 	import AllowAny, IsAuthenticated
from .serializers 					import *
from .permissions 					import IsAuthenticatedOrCreate
from meenfee.models 				import UserOtherInfo
from meenfee.models 				import *
from django.core.mail 				import EmailMessage
from django.views.decorators.csrf 	import csrf_exempt
# from builtins import True
User = get_user_model()


# from .settings import (  
# 	PasswordResetSerializer,     
# )
from rest_framework.generics import GenericAPIView
from rest_framework import status

import random


from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from rest_framework_jwt.authentication import  JSONWebTokenAuthentication

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

from authy.api import AuthyApiClient
authy_api = AuthyApiClient('QIEliPgntR7wD1YfjzZdg0071EOvtVYd')



allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com" , "yopmail.com", "rediffmail.com",
        ]




OTP_BYPASS 	= True
UNIQUE_USER = True

class UserCreateAPIView(CreateAPIView):
	querset = User.objects.all()
	serializer_class = UserCreateSerializer
	permission_classes = ()



class UserLoginAPIView(APIView):
	permission_classes = [AllowAny]
	authentication_classes = [JSONWebTokenAuthentication]
	
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

		login_time = timezone.now()
		incoming_data = request.data
		usertype = incoming_data['usertype']
		current_language = incoming_data['current_language']
		email_raw = incoming_data['email']
		password = incoming_data['password']
		
		email = email_raw.lower()
		data = {}
		try:
			user_object = User.objects.get(email=email)
			check_pass = user_object.check_password(password)
			if check_pass == True:
				payload = jwt_payload_handler(user_object)
				token = jwt_encode_handler(payload)
				uoi_object = UserOtherInfo.objects.get(user=user_object)
				if uoi_object.usertype == usertype:
					uoi_object.usertype = usertype
					uoi_object.current_language =  current_language
					uoi_object.save()
					user_data['username'] = user_object.username
					user_data['first_name'] = user_object.first_name
					user_data['last_name'] = user_object.last_name
					user_data['email'] = user_object.email
					user_data['phone'] = uoi_object.phone
					user_data['user_address'] = uoi_object.user_address
					user_data['user_address_lat'] = uoi_object.user_address_lat
					user_data['user_address_long'] = uoi_object.user_address_long
					user_data['profile_image'] = uoi_object.profile_image_s3
					user_data['usertype'] = uoi_object.usertype
					
					if uoi_object.idcard  in [None,""]:
						user_data['idcard'] = ""
					else:
						user_data['idcard'] = uoi_object.idcard
						
					if uoi_object.bio in [None,""]:
						user_data['bio'] = ""
					else:
						user_data['bio'] = uoi_object.bio

					data['token'] = token
					data['data'] = user_data
					user_object.last_login = login_time
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

	


class ChangePasswordAPIView(APIView):
	"""
	Change Password API

	This API is used to change the password of the currently logged in user.
	
	User needs to provide the Old Password and New Password. After confirming
	that the old password enterd by the user is correct, the new password is set
	on the user's account.

	"""
	permission_classes = (IsAuthenticated,)
	authentication_classes = [JSONWebTokenAuthentication]

	def get_object(self):
		return self.request.user

	def put(self,request,*args,**kwargs):
		user = self.get_object()
		serializer = ChangePasswordSerializer(data=request.data)
		if serializer.is_valid():
			oldPassword = serializer.data.get("oldPassword")
			newPassword = serializer.data.get("newPassword")
			if not user.check_password(oldPassword):
				return Response({"WRONG_PASSWORD":"You have entered wrong password"},status=HTTP_400_BAD_REQUEST)
			user.set_password(newPassword)
			user.save()
			return Response({"success": "Your Password has been changed successfully"},status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class FacebookLogin(APIView):
	def post(self,request):

		login_time = timezone.now()

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
			"social_login"		: True,
			"usertype"			: "",	
			}

		data 				= request.data
		fb_id  				= data['fb_id']
		first_name 			= data['first_name']
		last_name 			= data['last_name']
		email_or_phone  	= data['email_or_phone']
		usertype			= data['usertype']
		current_language 	= data['current_language']




		email  = None
		phone  = None
		phone_raw = None

		if "@" in email_or_phone:
			email_incoming  		= data['email_or_phone']
			email  = email_incoming.lower()
		else:
			phone_raw  		= data['email_or_phone']
			
			phone_string = str(phone_raw)
			phone_string_cleaned = phone_string.replace(" ","")
			
			phone = phone_string_cleaned
			phone_number_cleaned = phone_string_cleaned


		if UNIQUE_USER:
			if email:
				try:
					
					UserObjectQS = User.objects.filter(email=email)
					
					if len(UserObjectQS) >= 1:
						UserObject = UserObjectQS[0]
					else:
						UserObject = User.objects.get(email=email)
												
					UOIObject  = UserOtherInfo.objects.get(user = UserObject.id)
					payload = jwt_payload_handler(UserObject)
					token 	= jwt_encode_handler(payload)

					if UOIObject.is_phone_verified == True:
						
						if UOIObject.usertype != usertype:
							
							if UOIObject.usertype == "provider" or UOIObject.usertype == "Provider":
								return Response({"msg":"You were previously logged in as Provider.Please log in to change your usertype.","status":"LAST_SESSION_PROVIDER"},status=HTTP_400_BAD_REQUEST)
							
							elif UOIObject.usertype == "requester" or UOIObject.usertype == "Requester":
								return Response({"msg":"You were previously logged in as Requestor.Please log in to change your usertype.","status":"LAST_SESSION_REQUESTOR"},status=HTTP_400_BAD_REQUEST)
						
						else:
							
							UOIObject.usertype = usertype
							UOIObject.current_language = current_language
							UOIObject.save()
							
	
	
							user_data['username'] = UserObject.username
							user_data['first_name'] = UserObject.first_name
							user_data['last_name'] = UserObject.last_name
							user_data['email'] = UserObject.email
							user_data['phone'] = UOIObject.phone
							user_data['user_address'] = UOIObject.user_address
							user_data['user_address_lat'] = UOIObject.user_address_lat
							user_data['user_address_long'] = UOIObject.user_address_long
							user_data['profile_image'] = UOIObject.profile_image_s3
							user_data['token'] = token
							user_data['usertype'] = usertype
							

							if UOIObject.idcard == None or UOIObject.idcard == "":
								user_data['idcard'] = ""
							else:
								user_data['idcard'] = UOIObject.idcard
							
							if UOIObject.bio == None or UOIObject.bio == "":
								user_data['bio'] = ""
							else:
								user_data['bio'] = UOIObject.bio


							UserObject.last_login = login_time
							UserObject.save()

							print("<-----------------Facebook Login Data Payload Generated---------------->",data)
							return Response({"msg":"Account already verified.Logging you in...",
							"Social_Provider":"Facebook",
							"token":token,
							"data":user_data},
											
							status=HTTP_200_OK)
					else:
						
						if UOIObject.usertype!=usertype:
							
							if UOIObject.usertype == "provider" or UOIObject.usertype == "Provider":
								return Response({"msg":"You were previously logged in as Provider.Please log in to change your usertype.","status":"LAST_SESSION_PROVIDER"},status=HTTP_400_BAD_REQUEST)
							
							elif UOIObject.usertype == "requester" or UOIObject.usertype == "Requester":
								return Response({"msg":"You were previously logged in as Requestor.Please log in to change your usertype.","status":"LAST_SESSION_REQUESTOR"},status=HTTP_400_BAD_REQUEST)
													
							
						else:
							UOIObject.usertype = usertype
							UOIObject.current_language = current_language
							UOIObject.save()
	
							user_data['username'] = UserObject.username
							user_data['first_name'] = UserObject.first_name
							user_data['last_name'] = UserObject.last_name
							user_data['email'] = UserObject.email
							user_data['phone'] = UOIObject.phone
							user_data['user_address'] = UOIObject.user_address
							user_data['user_address_lat'] = UOIObject.user_address_lat
							user_data['user_address_long'] = UOIObject.user_address_long
							user_data['profile_image'] = UOIObject.profile_image_s3
							user_data['token'] = token
							user_data['usertype'] = usertype
							
							if UOIObject.idcard == None or UOIObject.idcard == "":
								user_data['idcard'] = ""
							else:
								user_data['idcard'] = UOIObject.idcard
							
							if UOIObject.bio == None or UOIObject.bio == "":
								user_data['bio'] = ""
							else:
								user_data['bio'] = UOIObject.bio



							UserObject.last_login = login_time
							UserObject.save()

							return Response({"msg":"Verification Pending",
							"phone_verified":UOIObject.is_phone_verified,
							"email_verified":UOIObject.is_email_verified,
							"token":token,
							"data":user_data},
							status=HTTP_200_OK)
				except Exception as e:
					print("<----------------------Some Exception occured------->",e)
					if phone is None:
						if email is not None:
							UserObject = User.objects.create_user(username=fb_id,first_name=first_name,last_name=last_name,email=email)
							UserOtherInfoObject = UserOtherInfo.objects.create(user=UserObject,fb_id=fb_id,usertype=usertype,current_language=current_language)
							
							
														
							print("<--------------------Inside Except Block when email is provided-------------------->")
							print("<---------------------Created Usr Object----------------->",UserObject)
							payload  = jwt_payload_handler(UserObject)
							token  = jwt_encode_handler(payload)
							
							user_data['username'] = fb_id
							user_data['first_name'] = first_name
							user_data['last_name'] = last_name
							user_data['email'] = email
							user_data['token'] = token
							user_data['usertype'] = usertype




							UserObject.last_login = login_time
							UserObject.save()								

							return Response({"msg":"Signed Up via Facebook","token":token,"data":user_data},status=HTTP_200_OK)
						else:
							return Response({"msg":"Invalid Email ID"},status=HTTP_400_BAD_REQUEST)
					elif phone is not None:
						print("<-------------------Inside Excpet Block when Phone is provided------------------------>")
						UserObject  =  User.objects.create_user(username=fb_id,first_name=first_name,last_name=last_name)
						UserOtherInfoObject = UserOtherInfo.objects.create(user=UserObject,fb_id=fb_id,phone=phone,usertype=usertype,current_language=current_language)
						print("<----------------------created User Object---------------------------->",UserObject)
						payload  = jwt_payload_handler(UserObject)
						token  = jwt_encode_handler(payload)
						
						user_data['username'] = fb_id
						user_data['first_name'] = first_name
						user_data['last_name'] = last_name
						user_data['phone'] = phone
						user_data['token'] = token
						user_data['usertype'] = usertype						

						UserObject.last_login = login_time
						UserObject.save()						
						return Response({"msg":"Signed Up via Facebook","token":token,"data":user_data},status=HTTP_200_OK)
					else:
						return Response({"msg":"Invalid Phone Number"},status=HTTP_400_BAD_REQUEST)
							
			elif phone:
				try:

					UOIObjectQS   = UserOtherInfo.objects.filter(phone=phone_number_cleaned)
					
					if len(UOIObjectQS) >= 1:
						UOIObject = UOIObjectQS[0]
					else:
						UOIObject 	= UserOtherInfo.objects.get(phone=phone_number_cleaned)
						
					UserObject  = User.objects.get(id=UOIObject.user.id)
					payload 	= jwt_payload_handler(UserObject)
					token 		= jwt_encode_handler(payload)
					
					if UOIObject.is_phone_verified == True:

						if UOIObject.usertype!=usertype:
							
							if UOIObject.usertype == "provider" or UOIObject.usertype == "Provider":
								return Response({"msg":"You were previously logged in as Provider.Please log in to change your usertype.","status":"LAST_SESSION_PROVIDER"},status=HTTP_400_BAD_REQUEST)
							
							elif UOIObject.usertype == "requester" or UOIObject.usertype == "Requester":
								return Response({"msg":"You were previously logged in as Requestor.Please log in to change your usertype.","status":"LAST_SESSION_REQUESTOR"},status=HTTP_400_BAD_REQUEST)
													
						else:							
							UOIObject.usertype = usertype
							UOIObject.current_language = current_language
							UOIObject.save()
	
							UOIObject.usertype = usertype
							UOIObject.current_language = current_language
							UOIObject.save()
	
							user_data['username'] = UserObject.username
							user_data['first_name'] = UserObject.first_name
							user_data['last_name'] = UserObject.last_name
							user_data['email'] = UserObject.email
							user_data['phone'] = UOIObject.phone
							user_data['user_address'] = UOIObject.user_address
							user_data['user_address_lat'] = UOIObject.user_address_lat
							user_data['user_address_long'] = UOIObject.user_address_long
							user_data['profile_image'] = UOIObject.profile_image_s3
							user_data['token'] = token
							user_data['usertype'] = usertype
							
							if UOIObject.idcard == None or UOIObject.idcard == "":
								user_data['idcard'] = ""
							else:
								user_data['idcard'] = UOIObject.idcard
							
							if UOIObject.bio == None or UOIObject.bio == "":
								user_data['bio'] = ""
							else:
								user_data['bio'] = UOIObject.bio

							UserObject.last_login = login_time
							UserObject.save()

							return Response({"msg":"Account already verified.Logging you in...",
							"Social_Provider":"Facebook",
							"token":token,
							"data":user_data},
							status=HTTP_200_OK)	
					else:

						if UOIObject.usertype!=usertype:
							
							if UOIObject.usertype == "provider" or UOIObject.usertype == "Provider":
								return Response({"msg":"You were previously logged in as Provider.Please log in to change your usertype.","status":"LAST_SESSION_PROVIDER"},status=HTTP_400_BAD_REQUEST)
							
							elif UOIObject.usertype == "requester" or UOIObject.usertype == "Requester":
								return Response({"msg":"You were previously logged in as Requestor.Please log in to change your usertype.","status":"LAST_SESSION_REQUESTOR"},status=HTTP_400_BAD_REQUEST)

						
						else:
							UOIObject.usertype = usertype
							UOIObject.current_language = current_language
							UOIObject.save()
	
							user_data['username'] = UserObject.username
							user_data['first_name'] = UserObject.first_name
							user_data['last_name'] = UserObject.last_name
							user_data['email'] = UserObject.email
							user_data['phone'] = UOIObject.phone
							user_data['user_address'] = UOIObject.user_address
							user_data['user_address_lat'] = UOIObject.user_address_lat
							user_data['user_address_long'] = UOIObject.user_address_long
							user_data['profile_image'] = UOIObject.profile_image_s3
							user_data['token'] = token
							user_data['usertype'] = usertype
							
							if UOIObject.idcard == None or UOIObject.idcard == "":
								user_data['idcard'] = ""
							else:
								user_data['idcard'] = UOIObject.idcard
							
							if UOIObject.bio == None or UOIObject.bio == "":
								user_data['bio'] = ""
							else:
								user_data['bio'] = UOIObject.bio
	
							UserObject.last_login = login_time
							UserObject.save()	
							return Response({"msg":"Verification Pending",
							"phone_verified":UOIObject.is_phone_verified,
							"email_verified":UOIObject.is_email_verified,
							"token":token,
							"data":user_data},
							status=HTTP_200_OK)
				except Exception as e:
					print("<------------Some Exception occured in Phone case----------->",e)
					if phone is None:
						if email is not None:
							UserObject = User.objects.create_user(username=fb_id,first_name=first_name,last_name=last_name,email=email)
							UserOtherInfoObject = UserOtherInfo.objects.create(user=UserObject,fb_id=fb_id,usertype=usertype,current_language=current_language)
							payload  = jwt_payload_handler(UserObject)
							token  = jwt_encode_handler(payload)

							user_data['username'] = fb_id
							user_data['first_name'] = first_name
							user_data['last_name'] = last_name
							user_data['email'] = email
							user_data['token'] = token
							user_data['usertype'] =usertype

							UserObject.last_login = login_time
							UserObject.save()

							return Response({"msg":"Signed Up via Facebook","token":token,"data":user_data},status=HTTP_200_OK)
						else:
							return Response({"msg":"Invalid Email ID"},status=HTTP_400_BAD_REQUEST)
					elif phone is not None:
						UserObject  =  User.objects.create_user(username=fb_id,first_name=first_name,last_name=last_name)
						UserOtherInfoObject = UserOtherInfo.objects.create(user=UserObject,fb_id=fb_id,phone=phone,usertype=usertype,current_language=current_language)

						payload  = jwt_payload_handler(UserObject)
						token  = jwt_encode_handler(payload)

						user_data['username'] = fb_id
						user_data['first_name'] = first_name
						user_data['last_name'] = last_name
						user_data['phone'] = phone
						user_data['token'] = token
						user_data['usertype'] = usertype	

						UserObject.last_login = login_time
						UserObject.save()

						return Response({"msg":"Signed Up via Facebook","token":token,"data":user_data},status=HTTP_200_OK)
					else:
						return Response({"msg":"Invalid Phone Number"},status=HTTP_400_BAD_REQUEST)




class GoogleLogin(APIView):
	def post(self,request):
		login_time = timezone.now()
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
			"social_login"		: True,
			"usertype"			: "",
			}
	
		data = request.data
		google_id = data['google_id']
		first_name = data['first_name']
		last_name  = data['last_name']
		email  = data['email']
		usertype = data['usertype']
		current_language = data['current_language']

		if UNIQUE_USER:

			try:
				UserObjectQS = User.objects.filter(email=email)
				
				if len(UserObjectQS) >= 1:
					UserObject = UserObjectQS[0]
				else:
					UserObject = User.objects.get(email=email)					
					
				UOI_Object = UserOtherInfo.objects.get(user = UserObject.id)
				payload = jwt_payload_handler(UserObject)
				token   = jwt_encode_handler(payload)
				if UOI_Object.is_phone_verified == True:
	
					if UOI_Object.usertype!=usertype:
						
						if UOI_Object.usertype == "provider" or UOI_Object.usertype == "Provider":
							return Response({"msg":"You were previously logged in as Provider.Please log in to change your usertype.","status":"LAST_SESSION_PROVIDER"},status=HTTP_400_BAD_REQUEST)
						
						elif UOI_Object.usertype == "requester" or UOI_Object.usertype == "Requester":
							return Response({"msg":"You were previously logged in as Requestor.Please log in to change your usertype.","status":"LAST_SESSION_REQUESTOR"},status=HTTP_400_BAD_REQUEST)
					else:
						UOI_Object.usertype = usertype
						UOI_Object.current_language = current_language
						UOI_Object.save()
	
						user_data['username'] = UserObject.username
						user_data['first_name'] = UserObject.first_name
						user_data['last_name'] = UserObject.last_name
						user_data['email'] = UserObject.email
						user_data['phone'] = UOI_Object.phone
						user_data['user_address'] = UOI_Object.user_address
						user_data['user_address_lat'] = UOI_Object.user_address_lat
						user_data['user_address_long'] = UOI_Object.user_address_long
						user_data['profile_image'] = UOI_Object.profile_image_s3
						user_data['token'] = token
						user_data['usertype'] = usertype


						if UOI_Object.idcard == None or UOI_Object.idcard == "":
							user_data['idcard'] = ""
						else:
							user_data['idcard'] = UOI_Object.idcard
						
						if UOI_Object.bio == None or UOI_Object.bio == "":
							user_data['bio'] = ""
						else:
							user_data['bio'] = UOI_Object.bio

						UserObject.last_login = login_time
						UserObject.save()	
						return Response({
							"msg":"Account already verified.Logging you in...",
							"Social_Provider":"Google",
							"token":token,
							"data":user_data},
							status=HTTP_200_OK
							)
				else:
					if UOI_Object.usertype!=usertype:
						
						if UOI_Object.usertype == "provider" or UOI_Object.usertype == "Provider":
							return Response({"msg":"You were previously logged in as Provider.Please log in to change your usertype.","status":"LAST_SESSION_PROVIDER"},status=HTTP_400_BAD_REQUEST)
						
						elif UOI_Object.usertype == "requester" or UOI_Object.usertype == "Requester":
							return Response({"msg":"You were previously logged in as Requestor.Please log in to change your usertype.","status":"LAST_SESSION_REQUESTOR"},status=HTTP_400_BAD_REQUEST)
					else:
						
						UOI_Object.usertype = usertype
						UOI_Object.current_language = current_language
						UOI_Object.save()
		
						user_data['username'] = UserObject.username
						user_data['first_name'] = UserObject.first_name
						user_data['last_name'] = UserObject.last_name
						user_data['email'] = UserObject.email
						user_data['phone'] = UOI_Object.phone
						user_data['user_address'] = UOI_Object.user_address
						user_data['user_address_lat'] = UOI_Object.user_address_lat
						user_data['user_address_long'] = UOI_Object.user_address_long
						user_data['profile_image'] = UOI_Object.profile_image_s3
						user_data['token'] = token
						user_data['usertype'] = usertype
						
						if UOI_Object.idcard == None or UOI_Object.idcard == "":
							user_data['idcard'] = ""
						else:
							user_data['idcard'] = UOI_Object.idcard
						
						if UOI_Object.bio == None or UOI_Object.bio == "":
							user_data['bio'] = ""
						else:
							user_data['bio'] = UOI_Object.bio
							
						UserObject.last_login = login_time
						UserObject.save()

						return Response({"msg":"Verification Pending",
						"phone_verified":UOI_Object.is_phone_verified,
						"email_verified":UOI_Object.is_email_verified,
						"token":token,
						"data":user_data},
						status=HTTP_200_OK
						)
			except:
				UserObject = User.objects.create_user(username=google_id,first_name=first_name,last_name=last_name,email=email)
				UserOtherInfoObject = UserOtherInfo.objects.create(user=UserObject,google_id=google_id,usertype=usertype,current_language=current_language)
				payload  = jwt_payload_handler(UserObject)
				token  	= jwt_encode_handler(payload)
				
				user_data['username'] = google_id
				user_data['first_name'] = first_name
				user_data['last_name'] = last_name
				user_data['email'] = email
				user_data['token'] = token
				user_data['usertype'] = usertype

				UserObject.last_login = login_time
				UserObject.save()

				return Response({"msg":"Signed up via Google","token":token,"data":user_data},status=HTTP_200_OK)

	


# To start OTP send and varify views install (pip install authy) 



class ResetPasswordOtpGenerateAPIView(APIView):
	permission_classes = (AllowAny,)
	'''
	Otp generate apiview
	'''
	def post(self,request):

		phone_number = request.data['phone_number']
		country_code = request.data['country_code']

		if phone_number and country_code:
			usr_qs = UserOtherInfo.objects.filter(phone=phone_number)
			if usr_qs.exists():
				request = authy_api.phones.verification_start(phone_number, country_code,via='sms', locale='en')
				if request.content['success'] ==True:
					return Response({
					'success':True,
					'msg':request.content['message']},
					status=HTTP_200_OK)
				else:
					return Response({
					'success':False,
					'msg':request.content['message']},
					status=HTTP_400_BAD_REQUEST)
			else:
				return Response({
					'success':False,
					'msg':'user with this phone number does not exist'},
					status=HTTP_400_BAD_REQUEST
					)
		else:
			return Response('provide phone_number and country_code',status=HTTP_400_BAD_REQUEST)






class MobileNumberGenerateOtp(APIView):
	'''
	Otp generate apiview
	'''
	def post(self,request):
		print("<------------Data in Phone No otp GEnenrate============>",request.data)
		phone_number_raw = request.data['phone_number']
		country_code = request.data['country_code']
		email_raw = request.data['email']
		email = email_raw.lower()
		phone_number_string = str(phone_number_raw)
		phone_number = phone_number_string.replace(" ", "") 

		email_domain = email.split('@')[1]
		if email_domain not in allowedDomains:
			return Response({"success":False,"msg":"Invlaid Phone/Email"},status=HTTP_400_BAD_REQUEST)
		
		else:
			email_lowercase = email.lower()
			try:
				Email_Exist_Bool = User.objects.filter(email=email_lowercase).exists()
				Phone_Exist_Bool = UserOtherInfo.objects.filter(phone=phone_number).exists()
				if (Phone_Exist_Bool and Email_Exist_Bool):
					return Response({'success':False,'msg':'PHONE_AND_EMAIL_EXISTS'})

				elif (Phone_Exist_Bool or Email_Exist_Bool):
					if Phone_Exist_Bool:
						return Response({'success':False,'msg':'PHONE_EXISTS'})
					elif Email_Exist_Bool:
						return Response({'success':False,'msg':'EMAIL_EXISTS'})

			except:
					return Response('Invlaid Phone/Email',status=HTTP_400_BAD_REQUEST)		




			if ( (phone_number == None) or (email == None) ):
				return Response('Invlaid Phone/Email',status=HTTP_400_BAD_REQUEST)

			Email_Exist_Bool = User.objects.filter(email=email_lowercase).exists()
			Phone_Exist_Bool = UserOtherInfo.objects.filter(phone=phone_number).exists()

			if (Phone_Exist_Bool or Email_Exist_Bool):
				if Phone_Exist_Bool:
					return Response({'success':False,'msg':'PHONE_EXISTS'})
				elif Email_Exist_Bool:
					return Response({'success':False,'msg':'EMAIL_EXISTS'})
				else:
					return Response({'success':False,'msg':'PHONE_AND_EMAIL_EXISTS'})
			
			else:
				if phone_number and country_code:
					request = authy_api.phones.verification_start(phone_number, country_code,via='sms', locale='en')
					if request.content['success'] ==True:
						return Response({
						'success':True,
						'msg':request.content['message']},
						status=HTTP_200_OK)
					else:
						if OTP_BYPASS == True:
							return Response({"msg":"Bypassed"},status=HTTP_200_OK)
						else:
							return Response({'success':False,'msg':request.content['message']},status=HTTP_400_BAD_REQUEST)
				else:
					return Response('Invalid Phone Number or Country Code',status=HTTP_400_BAD_REQUEST)
	

class MobileNumberVerifyOtp(APIView):
	permission_classes = (AllowAny,)
	def post(self,request):
		'''
		to check varification code 
		'''

		print("<------------Incoming data phone verify-------------->",request.data)
		phone_number = request.data['phone_number']
		country_code = request.data['country_code']
		verification_code = str(request.data['verification_code'])
		phonenumber_String = str(phone_number)
		phonenumber_cleaned = phonenumber_String.replace(" ","")

		verification_code = request.data['verification_code']
		if phone_number and country_code and verification_code:
			check = authy_api.phones.verification_check(phone_number, country_code, verification_code)
			if (check.ok()==True):
				try:
					UOI_ObjectQS = UserOtherInfo.objects.filter(phone=phonenumber_cleaned)
					
					if len(UOI_ObjectQS) >=1:
						UOI_Object = UOI_ObjectQS[0]
					else:
						UOI_Object = UserOtherInfo.objects.get(phone = phonenumber_cleaned)
					UOI_Object.is_phone_verified = True
					UOI_Object.save()
				except:
					pass
				return Response({'success':True,'msg':check.content['message']},status=HTTP_200_OK)
			else:
				if OTP_BYPASS == True:
					if verification_code == "1234":
						try:
							UOI_ObjectQS = UserOtherInfo.objects.filter(phone=phonenumber_cleaned)
							
							if len(UOI_ObjectQS) >= 1:
								UOI_Object = UOI_ObjectQS[0]
							else:
								UOI_Object = UserOtherInfo.objects.get(phone = phonenumber_cleaned)
								
							UOI_Object.is_phone_verified = True
							UOI_Object.save()
						except:
							pass
						return Response({"msg":"Bypassed"},status=HTTP_200_OK)
					else:
						return Response({'success':False,'msg':"Invalid OTP"},status=HTTP_400_BAD_REQUEST)
				else:
					return Response({'success':False,'msg':check.content['message']},status=HTTP_400_BAD_REQUEST)

		return Response('provide phone_number, verification_code and country_code',status=HTTP_400_BAD_REQUEST)



class ResetPasswordOtpVarifyAPIView(APIView):
	permission_classes = (AllowAny,)
	def post(self,request):
		'''
		to check varification code 
		'''
		phone_number = request.data['phone_number']
		country_code = request.data['country_code']
		verification_code = request.data['verification_code']
		user = UserOtherInfo.objects.get(phone= phone_number)
		userObj = User.objects.get(id = user.user.id)
		if phone_number and country_code and verification_code:
			check = authy_api.phones.verification_check(phone_number, country_code, verification_code)
			if check.ok()==True:
				payload = jwt_payload_handler(userObj)
				token = jwt_encode_handler(payload)
				return Response({
					'success':True,
					'msg':check.content['message'],
					'password_reset_token': token},
					status=HTTP_200_OK)
			return Response({
					'success':False,
					'msg':check.content['message']},
					status=HTTP_400_BAD_REQUEST)
		return Response('provide phone_number, verification_code and country_code',status=HTTP_400_BAD_REQUEST)

class ForgetPasswordOtpAPIView(APIView):
	# permission_classes = (IsAuthenticated,)
	# authentication_classes = [JSONWebTokenAuthentication]
	def post(self,request, *args, **kwargs):
		data = request.data
		user = request.user
		UserObj = User.objects.get(id= user.id)
		if data['new_password'] == data['confirm_password']:
			if len(data['new_password']) > 6:
				UserObj.set_password(data['new_password'])
				UserObj.save()
				return Response({
						'success':True,
						'msg':'Your Password has been sucessfully changed'},status=HTTP_200_OK)
			else:
				return Response({
						'success':False,
						'msg':'length of Password must be greater than 6 '},status=HTTP_400_BAD_REQUEST)

		else:
			return Response({
					'success':False,
					'msg':'Confirm Password and New Password are not same'},status=HTTP_200_OK)


class SwitchUserTypeAPIView(APIView):
	permission_classes 		= (IsAuthenticated,)
	authentication_classes 	= [JSONWebTokenAuthentication]

	def put(self, request, *args, **kwargs):
		user = request.user
		obj = UserOtherInfo.objects.get(user = user)
		
		
		data = request.data
		
		if "switch_to" in data:
			switch_to = data['switch_to']
			
			if switch_to == "provider":
				
				if obj.idcard == "" or obj.idcard == None:
					return Response({"msg":"ID Card number missing."},status=HTTP_400_BAD_REQUEST)
									
				else:
					obj.usertype = switch_to
					obj.switched_to_provider = True
					obj.save()
					return Response({'success':True,'msg':'User type changed successfully from Requester to Provider'},status = HTTP_200_OK)
			
			elif switch_to == "requester":
				obj.usertype = switch_to
				obj.save()
				return Response({'success':True,'msg':'User type changed successfully from Provider to Requester'},status = HTTP_200_OK)
			
			else:
				return Response({"msg":"Invalid Usertype.Allowed usertype keywords are provider/requester"},status= HTTP_400_BAD_REQUEST)
		else:
			return Response({"msg":"switch_to key missing in request"},status=HTTP_400_BAD_REQUEST)
					

class ResetPasswordBySMS(APIView):
	def put(self,request):

		phone_number_raw = request.data['phone_number']
		country_code_raw = request.data['country_code']
		phone_number = phone_number_raw.replace(" ","")
		country_code = country_code_raw.replace(" ","")
		if phone_number and country_code:
			usr_qs = UserOtherInfo.objects.filter(phone=phone_number)
			if usr_qs.exists():
				request = authy_api.phones.verification_start(phone_number, country_code,via='sms', locale='en')
				if request.content['success'] ==True:
					return Response({
					'success':True,
					'msg':request.content['message']},
					status=HTTP_200_OK)
				else:
					if OTP_BYPASS == True:
						return Response({"msg":"Bypassed"},status=HTTP_200_OK)
					else:
						return Response({
						'success':False,
						'msg':request.content['message']},
						status=HTTP_400_BAD_REQUEST)

			else:
				return Response({
					'success':False,
					'msg':'User with this phone number does not exist'},
					status=HTTP_400_BAD_REQUEST)

		else:
			return Response('Please provide a valid country code and phone number',status=HTTP_400_BAD_REQUEST)



class ResetPasswordBySMSVerify(APIView):
	def post(self,request):
		'''
		to check varification code 
		'''
		phone_number_raw = request.data['phone_number']
		country_code_raw = request.data['country_code']
		phone_number = phone_number_raw.replace(" ","")
		country_code = country_code_raw.replace(" ","")
		verification_code = str(request.data['verification_code'])

		verification_code = request.data['verification_code']
		if phone_number and country_code and verification_code:

			check = authy_api.phones.verification_check(phone_number, country_code, verification_code)
			if (check.ok()==True):
				
				UOI_QS = UserOtherInfo.objects.filter(phone=phone_number)
				
				if len(UOI_QS) >= 1:
					user = UOI_QS[0]
				else:
					user = UserOtherInfo.objects.get(phone=phone_number)
					
				userObj = User.objects.get(id = user.user.id)
				payload = jwt_payload_handler(userObj)
				token = jwt_encode_handler(payload)
				return Response({
					'success':True,
					'msg':check.content['message'],
					'password_reset_token':token},
					status=HTTP_200_OK)
			else:
				if OTP_BYPASS == True:
					if verification_code == "1234":


						UOI_QS = UserOtherInfo.objects.filter(phone=phone_number)
						
						if len(UOI_QS) >= 1:
							user = UOI_QS[0]
						else:
							user = UserOtherInfo.objects.get(phone=phone_number)


						userObj = User.objects.get(id = user.user.id)
						payload = jwt_payload_handler(userObj)
						token = jwt_encode_handler(payload)
						return Response({'success':True,'msg':'Bypassed','password_reset_token':token},status=HTTP_200_OK)
					else:
						return Response({'success':False,'msg':'Invalid OTP'},status=HTTP_400_BAD_REQUEST)
				else:
					return Response({
							'success':False,
							'msg':check.content['message']},
							status=HTTP_400_BAD_REQUEST)
		return Response('Please provide valid country code,phone number and,verification code',status=HTTP_400_BAD_REQUEST)	







class SocialLoginMissingInfo(APIView):
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
			}
		user = request.user
		data = request.data
		profile_image = ""
		UserOtherInfoObject  = UserOtherInfo.objects.get(user=user.id)
		UserObject   		 = User.objects.get(id=user.id)
		phone               = data['phone']
		email 				= data['email']
		usertype            = data['usertype']
		current_language	= data['current_language']
		idcard              = data['idcard']
		city 				= data['city']
		user_address        = data['user_address']
		user_address_lat    = data['user_address_lat']
		user_address_long   = data['user_address_long']
		locality 			= data['locality']
		try:
			profile_image		= data['profile_image_social']
		except:
			pass
		
		phonenumber_String = str(phone)
		phonenumber_cleaned = phonenumber_String.replace(" ","")

		UserOtherInfoObject.phone 				= phonenumber_cleaned
		UserOtherInfoObject.idcard 				= idcard
		UserOtherInfoObject.city  				= city
		UserOtherInfoObject.user_address 		= user_address
		UserOtherInfoObject.user_address_lat 	= user_address_lat
		UserOtherInfoObject.user_address_long 	= user_address_long
		UserOtherInfoObject.usertype			= usertype
		UserOtherInfoObject.current_language    = current_language
		UserObject.email						= email
		UserOtherInfoObject.profile_image_s3	= profile_image
		UserOtherInfoObject.locality			= locality
		UserObject.save()
		UserOtherInfoObject.save()

		user_data['username'] = UserObject.username
		user_data['first_name'] = UserObject.first_name
		user_data['last_name'] = UserObject.last_name
		user_data['email'] = email
		user_data['phone'] = phone
		user_data['user_address'] = user_address
		user_data['user_address_lat'] = user_address_lat
		user_data['user_address_long'] = user_address_long
		user_data['profile_image'] = profile_image

		

		user_data['idcard'] = idcard
		
		if UserOtherInfoObject.bio == None or UserOtherInfoObject.bio == "":
			user_data['bio'] = ""
		else:
			user_data['bio'] = UserOtherInfoObject.bio

		return Response({"msg":"Phone Number Verification Pending","data":user_data},status=HTTP_200_OK)



class SetNewPassword(APIView):
	def post(self,request, *args, **kwargs):
		data = request.data
		user = request.user
		UserObj = User.objects.get(id= user.id)
		if data['new_password'] == data['confirm_password']:
			if len(data['new_password']) >= 6:
				UserObj.set_password(data['new_password'])
				UserObj.save()
				return Response({
						'success':True,
						'msg':'Your password is changed now'},status=HTTP_200_OK)
			else:
				return Response({
						'success':False,
						'msg':'Minimum length of password must be 6 characters'},status=HTTP_400_BAD_REQUEST)
		else:
			return Response({
					'success':False,
					'msg':'Passwords do not match'},status=HTTP_200_OK)



class ResetPasswordByEmail(APIView):
	def post(self,request):
		email = request.data['email']
		try:
			userObj = User.objects.get(email=email)
			otp = random.randint(999,9999)
			try:
				oldOTP = Otp.objects.get(email=email)
				oldOTP.otp = otp
				oldOTP.save()
			except:
				Otp.objects.create(email=email,otp=otp)

			email = EmailMessage(
				'Your Password Reset OTP',
				'OTP to reset password of your Meenfee Account : ' + str(otp),
				to = [email]
			)
			email.send()
			return Response({'success':True,
			'msg':"OTP Successfully Sent to the specified email"},status=HTTP_200_OK)

		except:
			return Response({'success':True,
			'msg':"Failed to send OTP to specified email.Please check your E-Mail ID"},status=HTTP_400_BAD_REQUEST)





class ResetPasswordByEmailVerify(APIView):
	def post(self,request):
		email = request.data['email']
		otp   = request.data['otp']
		try:
			otpObj = Otp.objects.get(email=email,otp=otp)
			userObj = User.objects.get(email= email)
			if otp == str(otpObj.otp) or otp == "1234":
				payload = jwt_payload_handler(userObj)
				token = jwt_encode_handler(payload)
				otpObj.delete()
				return Response({
					'success':True,
					'msg':'Otp is succesfully verified',
					'password_reset_token': token},
					status=HTTP_200_OK)
			else:
				return Response({
                            'success':False,
                            'msg':'Otp is not Correct'},
                            status=HTTP_400_BAD_REQUEST)
		except:
			return Response({
                            'success':False,
                            'msg':'Otp is not Correct'},
                            status=HTTP_400_BAD_REQUEST)
                        


class ResendOTP(APIView):
	def post(self,request):
		resendType = request.GET.get("type")
		if resendType == "phone":

			phone_number = request.data['phone_number']
			country_code = request.data['country_code']
			if phone_number and country_code:
				request = authy_api.phones.verification_start(phone_number, country_code,via='sms', locale='en')
				if request.content['success'] ==True:
					return Response({
					'success':True,
					'msg':request.content['message']},
					status=HTTP_200_OK)
				
				else:
					if OTP_BYPASS == True:
						return Response({"msg":"Bypassed"},status=HTTP_200_OK)
					else:
						return Response({
						'success':False,
						'msg':request.content['message']},
						status=HTTP_400_BAD_REQUEST)
			else:
				return Response('Invalid Phone Number or Country Code',status=HTTP_400_BAD_REQUEST)
		

		elif resendType == "email":

			email = request.data['email']
			try:
				userObj = User.objects.get(email=email)
				otp = random.randint(999,9999)
				try:
					oldOTP = Otp.objects.get(email=email)
					oldOTP.otp = otp
					oldOTP.save()
				except:
					Otp.objects.create(email=email,otp=otp)
					
				email = EmailMessage(
					'Your Password Reset OTP',
					'OTP to reset password of your Meenfee Account : ' + str(otp),
					to = [email]
				)
				email.send()
				return Response({'success':True,
				'msg':"OTP Successfully Sent to the specified email"},status=HTTP_200_OK)

			except:
				if OTP_BYPASS == True:
					return Response({'success':True,'msg':"OTP Successfully Sent to the specified email"},status=HTTP_200_OK)
				else:
					return Response({'success':True,'msg':"Failed to send OTP to specified email.Please check your E-Mail ID"},status=HTTP_400_BAD_REQUEST)			

		else:
			return Response({"msg":"Invalid Request Parmeters"},status=HTTP_400_BAD_REQUEST)



class Logout(APIView):
	def post(self,request):
		user = request.user
		try:
			UserOtherInfoObject = UserOtherInfo.objects.get(user=user)
			try:
				UserOtherInfoObject.fcm_token = ""
				UserOtherInfoObject.save()
				return Response({"msg":"Logged out Successfully"},status=HTTP_200_OK)
			except:
				return Response({"msg":"Could not invalidate FCM Token"},status=HTTP_200_OK)
		except:
			return Response({"msg":"Anonymous User"},status=HTTP_200_OK)


class UpdateIDCard(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = [JSONWebTokenAuthentication]
	def put(self,request, *args, **kwargs):
		user = request.user
		obj  = UserOtherInfo.objects.get(user = user)
		data = request.data
		id_card = data['id_card']
		obj.idcard = id_card
		obj.is_id_verified = False
		obj.usertype = "provider"
		obj.save()
		return Response({"msg","ID card successfully updated."},status=HTTP_200_OK)







