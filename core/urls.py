from django.contrib import admin
from django.urls import path, re_path
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView, ConfirmEmailView
from accounts.views import CheckEmailUniqueView, UploadImageView, CustomUserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/rest-auth/registration', RegisterView.as_view(), name='rest_signup'),
    path('api/rest-auth/login', LoginView.as_view(), name='rest_login'),
    path('api/rest-auth/logout', LogoutView.as_view(), name='rest_logout'),
    path('api/rest-auth/password/change', PasswordChangeView.as_view(), name='rest_password_change'),
    path('api/rest-auth/unique', CheckEmailUniqueView.as_view(), name='rest_unique'),
    path('api/rest-auth/upload-image', UploadImageView.as_view(), name='rest_upload_image'),
    path('api/rest-auth/user', CustomUserDetailsView.as_view(), name="rest_profile"),
    path('api/rest-auth/token/verify', TokenVerifyView.as_view(), name="rest_verify_token"),
    
    # re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'), 
    # re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
]
