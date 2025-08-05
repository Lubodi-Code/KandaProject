from django.urls import path
from . import views
from . import api_views
from . import character_views
from . import monitoring_views

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
    
    # Rutas de API JSON - Gestión de personajes
    path('api/characters/', character_views.list_characters, name='list_characters'),
    path('api/characters/create/', character_views.create_character, name='create_character'),
    path('api/characters/<str:character_id>/', character_views.get_character, name='get_character'),
    path('api/characters/<str:character_id>/update/', character_views.update_character, name='update_character'),
    path('api/characters/<str:character_id>/delete/', character_views.delete_character, name='delete_character'),
    path('api/characters/<str:character_id>/status/', character_views.get_processing_status, name='get_processing_status'),
    path('api/characters/<str:character_id>/retry/', character_views.retry_processing, name='retry_processing'),
    path('api/characters/<str:character_id>/export/', character_views.export_character, name='export_character'),
    path('api/characters/<str:character_id>/export/<str:format>/', character_views.export_character, name='export_character_format'),
    
    # Rutas de API JSON - Monitoreo y estadísticas
    path('api/statistics/user/', monitoring_views.user_statistics, name='user_statistics'),
    path('api/statistics/admin/', monitoring_views.admin_statistics, name='admin_statistics'),
    path('api/system/health/', monitoring_views.system_health, name='system_health'),
]