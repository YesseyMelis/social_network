from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from apps.account.views import AuthViewSet

urlpatterns = []

router = routers.DefaultRouter()
router.register('v1/auth', AuthViewSet)

app_name = 'account'

urlpatterns += router.urls
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
