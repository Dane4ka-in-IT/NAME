from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.dashboard_view, name='manage_dashboard'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('tests/', views.TestListView.as_view(), name='test_list'),
    path('tests/<int:test_id>/start/', views.start_test, name='start_test'),
    path('tests/sessions/<int:session_id>/', views.question_view, name='question_view'),
    path('tests/sessions/<int:session_id>/results/', views.end_test, name='end_test'),
] 