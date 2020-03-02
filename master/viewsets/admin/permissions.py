from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()

class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):

	def test_func(self):
		return self.request.user.is_superuser and self.request.user.user_type == User.ADMIN