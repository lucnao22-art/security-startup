# workflow/urls.py

from django.urls import path
from . import views

app_name = 'workflow'

urlpatterns = [
    # URLs cho Công việc (Task)
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/new/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),

    # URLs cho Đề xuất (Proposal)
    path('proposals/', views.ProposalListView.as_view(), name='proposal_list'),
    path('proposals/new/', views.ProposalCreateView.as_view(), name='proposal_create'),
    path('proposals/<int:pk>/', views.ProposalDetailView.as_view(), name='proposal_detail'),
    path('proposals/<int:pk>/review/', views.ProposalReviewView.as_view(), name='proposal_review'),
]