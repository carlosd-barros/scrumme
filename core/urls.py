from django.views.generic.base import RedirectView
from django.urls import path, re_path

from core.views.base import DashboardView, NotFoundView

from core.views.equipe import (
    EquipeCreateView, EquipeDeleteView,
    EquipeDetailView, EquipeListView,
    EquipeUpdateView
)
from core.views.quest import (
    QuestCreateView, QuestDeleteView,
    QuestDetailView, QuestListView,
    QuestUpdateView
)
from core.views.jogador import (
    JogadorCreateView, JogadorDeleteView,
    JogadorDetailView, JogadorListView,
    JogadorUpdateView
)

app_name='core'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    # Jogador
    path(
        'profile/<int:pk>/details/',
        JogadorDetailView.as_view(),
        name='jogador_details'
    ),
    path(
        'profile/<int:pk>/update/',
        JogadorUpdateView.as_view(),
        name='jogador_update'
    ),

    # Quest


    # Equipe
    path(
        'equipe/create',
        EquipeCreateView.as_view(),
        name='equipe_create'
    ),


    # Classe


    # http erros
    path('404/', NotFoundView.as_view(), name='404'),
]