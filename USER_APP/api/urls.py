from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from USER_APP.api.views import CreateUserView, LoginView, ChangePasswordView, UpdatePasswordByUserView, ResetForgotPasswordView, Logout, UserInfoView, AddBitacoraRegistro
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('create-user/', CreateUserView.as_view() , name='create-user'),
    path('login/',LoginView.as_view() , name ='login'),
    path('change-password/',ChangePasswordView.as_view() , name ='change-password'),
    path('update-password-by-user/',UpdatePasswordByUserView .as_view() , name ='update-password-by-user'),
    path('forgot-password-token/',ResetForgotPasswordView.as_view() , name ='forgot-password-token'),
    path('logout/',Logout.as_view() , name ='logout'),
    path('user-info/',UserInfoView.as_view() , name ='user-info'),
    
    
    path('add-registro-bitacora/',AddBitacoraRegistro.as_view() , name ='add-registro-bitacora'),

    path('api/token/',TokenObtainPairView.as_view() , name ='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view() , name ='token_refresh'),
]