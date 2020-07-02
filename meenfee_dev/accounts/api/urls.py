
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('register/',UserCreateAPIView.as_view(),name="register"),
	path('login/',UserLoginAPIView.as_view(),name="login"),
	path('changepassword/',ChangePasswordAPIView.as_view(),name="changePassword"),
    path('otp-generate',ResetPasswordOtpGenerateAPIView.as_view(),name="OtpGenerateAPIView"),
    path('otp-verify',ResetPasswordOtpVarifyAPIView.as_view(),name="OtpVarifyAPIView"),
    path('change/usertype',SwitchUserTypeAPIView.as_view(),name="SwitchUserType"),
    path('password/reset/otp',ForgetPasswordOtpAPIView.as_view(),name='ChangePassword'),
    path('phone-no/otp-generate',MobileNumberGenerateOtp.as_view(),name='MobileNumberOtpGeneration'),  #To Be Enabled in Production
    path('phone-no/otp-verify',MobileNumberVerifyOtp.as_view(),name='MobileNumberVerification'),
    path('resetPassword/sms/otp-generate',ResetPasswordBySMS.as_view(),name="Reset Password OTP Generate"),
    path('resetPassword/sms/otp-verify',ResetPasswordBySMSVerify.as_view(),name="Reset Password Verify"),
    path('setPassword',SetNewPassword.as_view(),name="Set Password"),
    path('resetPassword/email/otp-generate',ResetPasswordByEmail.as_view(),name="Reset Password By Email OTP Generate"),
    path('resetPassword/email/otp-verify',ResetPasswordByEmailVerify.as_view(),name="Reset Password By Email OTP Verify"),
    path('resend/otp',ResendOTP.as_view(),name="Resend OTP"),
    path('update_missing_info/',SocialLoginMissingInfo.as_view(),name="Social Login Missing Info"),
    path('social_login/facebook/',FacebookLogin.as_view(),name="Facebook Login"),
    path('social_login/google/',GoogleLogin.as_view(),name="Google Login"),
    path('logout/',Logout.as_view(),name="Logout"),
    path('update/idcard',UpdateIDCard.as_view(),name="UpdateIDCard")
]