from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from apps.account.models import User


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            User.objects.filter(id=request.user.id).update(last_activity=timezone.now())
