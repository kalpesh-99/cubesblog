from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
	message = "You must be the owner of this post."
	my_safe_method = ['GET', 'PUT', 'DELETE'] # added delete to safe method
	def has_permission(self, request, view): # has permission is similar to object permisson but in case we didn't have object view
		if request.method in self.my_safe_method:
			return True
		return False


	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True

		return obj.user == request.user
