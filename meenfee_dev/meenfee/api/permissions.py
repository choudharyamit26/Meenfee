from rest_framework.permissions import BasePermission,SAFE_METHODS
from meenfee.models import UserOtherInfo

class IsOwnerOrReadOnly(BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		return obj.user == request.user


class IsUser(BasePermission):
	def has_permission(self, request, view):
	
		if 'HTTP_USER_AGENT' in request.META:
			# print (request.META[''])
			if 'Mozilla' in request.META['HTTP_USER_AGENT']:
				if(request.META.get('HTTP_REFERER')):
					return True
		return False

class IsProvider(BasePermission):
	message = 'You are requester please switch your account to provider to access this service '
	def has_permission(self, request, view):
		try:
			objet = UserOtherInfo.objects.get(user=request.user)
			if objet.usertype=='provider':
				print('ok')
				return True
			return False
		except:
			return False


class IsRequester(BasePermission):
	message = 'You are provider please switch your account to requester to access this service '
	def has_permission(self, request, view):
		try:
			obj=UserOtherInfo.objects.get(user=request.user)
			if obj.usertype =='requester':
				return True
			return False
		except:
			return False