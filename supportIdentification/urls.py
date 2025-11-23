from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.logar, name='login'),
    path('cadastro/', views.cadastrar, name='cadastro'),
    path('perfil/', views.visualizar, name='visualizar'),
    path('perfil/editar/', views.editar, name='editar'),
    path('perfil/sair/', views.deslogar, name='deslogar')
]