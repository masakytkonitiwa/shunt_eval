from django.contrib import admin
from django.urls import path, include  # ← include を追加
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient/', include('patient.urls')),  # ← これを追加
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
        # 👇 "/" にアクセス → dashboard に飛ぶ（ログインしてなければログイン画面になる）
    path('', lambda request: redirect('dashboard')),

]