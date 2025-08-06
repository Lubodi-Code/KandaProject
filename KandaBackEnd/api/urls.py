from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import views, api_views, monitoring_views
from .views.character_views import CharacterViewSet, create_default_character

router = DefaultRouter()
router.register(r'characters', CharacterViewSet, basename='character')

urlpatterns = [
    # Rutas de prueba
    path('test-connection/', views.test_connection, name='test_connection'),
    path('test-models/', views.test_model_view, name='test_model_view'),

    # Rutas de autenticación (vistas tradicionales)
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Rutas de activación de cuenta
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
    path('resend-activation/', views.resend_activation, name='resend_activation'),

    # Rutas de API JSON - Autenticación
    path('api-login/', api_views.api_login, name='api_login'),
    path('api-register/', api_views.api_register, name='api_register'),
    path('api-dashboard/', api_views.api_dashboard, name='api_dashboard'),
    path('api-activate/<str:uidb64>/<str:token>/', api_views.api_activate_account, name='api_activate'),
    path('api-resend-activation/', api_views.api_resend_activation, name='api_resend_activation'),

    # Rutas de API JSON - Monitoreo y estadísticas
    path('api/statistics/user/', monitoring_views.user_statistics, name='user_statistics'),
    path('api/statistics/admin/', monitoring_views.admin_statistics, name='admin_statistics'),
    path('api/system/health/', monitoring_views.system_health, name='system_health'),

    # Rutas de API JSON - Gestión de personajes
    path('', include(router.urls)),
    path('characters/create-default/', create_default_character, name='create_default_character'),
]
