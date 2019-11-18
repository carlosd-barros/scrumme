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
    QuestUpdateView, QuestComplete
)
from core.views.jogador import (
    JogadorDeleteView,
    JogadorDetailView, JogadorListView,
    JogadorUpdateView
)
from core.views.classe import (
    ClasseCreateView, ClasseDeleteView,
    ClasseDetailView, ClasseListView,
    ClasseUpdateView
)


app_name='core'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),

    # Jogador
    path(
        'profile/<int:pk>/details/',
        JogadorDetailView.as_view(),
        name='jogador_detail'
    ),
    path(
        'profile/<int:pk>/update/',
        JogadorUpdateView.as_view(),
        name='jogador_update'
    ),
    path(
        'profile/<int:pk>/delete/',
        JogadorDeleteView.as_view(),
        name='jogador_delete'
    ),

    # Quest
    path(
        'quest/list/',
        QuestListView.as_view(),
        name='quest_list'
    ),
    path(
        'quest/create/',
        QuestCreateView.as_view(),
        name='quest_create'
    ),
    path(
        'quest/<int:pk>/delete/',
        QuestDeleteView.as_view(),
        name='quest_delete'
    ),
    path(
        'quest/<int:pk>/detail/',
        QuestDetailView.as_view(),
        name='quest_detail'
    ),
    path(
        'quest/<int:pk>/update',
        QuestUpdateView.as_view(),
        name='quest_update'
    ),
    path(
        'quest/<int:pk>/complete',
        QuestComplete.as_view(),
        name = 'quest_complete'
    ),


    # Equipe
    path(
        'equipe/list/',
        EquipeListView.as_view(),
        name='equipe_list'
    ),
    path(
        'equipe/create/',
        EquipeCreateView.as_view(),
        name='equipe_create'
    ),
    path(
        'equipe/<int:pk>/delete/',
        EquipeDeleteView.as_view(),
        name='equipe_delete'
    ),
    path(
        'equipe/<int:pk>/detail/',
        EquipeDetailView.as_view(),
        name='equipe_detail'
    ),
    path(
        'equipe/<int:pk>/update/',
        EquipeUpdateView.as_view(),
        name='equipe_update'
    ),


    # Classe
    path(
        'classe/list/',
        ClasseListView.as_view(),
        name='classe_list'
    ),
    path(
        'classe/create/',
        ClasseCreateView.as_view(),
        name='classe_create'
    ),
    path(
        'classe/<int:pk>/delete/',
        ClasseDeleteView.as_view(),
        name='classe_delete'
    ),
    path(
        'classe/<int:pk>/detail/',
        ClasseDetailView.as_view(),
        name='classe_detail'
    ),
    path(
        'classe/<int:pk>/update/',
        ClasseUpdateView.as_view(),
        name='classe_update'
    ),


    # http erros
    path('404/', NotFoundView.as_view(), name='404'),
]