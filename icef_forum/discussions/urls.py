from django.urls import path
from . import views
app_name = 'discussions'

urlpatterns = [
    path('', views.index, name='index'),
    path('professors/<slug:slug>/', views.professor_discussion, name='professor'),
    path('professors/', views.professors_list, name='professors_list'),
    path('professors/search/', views.professors_search, name='professors_search'),
    path('professors/rating/<slug:slug>/', views.professors_rating, name='professors_rating'),
    path('professors/<slug:slug>/write/', views.professor_write, name='professor_write'),
    path('professors/<slug:slug>/approve/', views.professor_approve, name='professor_approve'),
    path('professors/<slug:slug>/disapprove/', views.professor_disapprove, name='professor_disapprove'),
    path('posts/<int:post_id>/rate/', views.post_rate, name='post_rate'),
    path('posts/<int:post_id>/detail/', views.post_detail, name='post_detail'),
    path(
        'posts/<int:post_id>/comment/', views.add_comment, name='add_comment'
    ),
    path('courses/<slug:slug>/', views.course_discussion, name='course'),
    path('courses/<slug:slug>/write/', views.course_write, name='course_write'),
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/search/', views.courses_search, name='courses_search'),
    path('jobs/<slug:slug>/', views.job_discussion, name='job'),
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/<slug:slug>/vacancies', views.job_vacancies, name='job_vacancies'),
    path('jobs/<slug:slug>/write/', views.job_write, name='job_write'),
    path('vacancies/', views.vacancy_list, name='vacancy_list'),
    path('vacancies/create/', views.create_vacancy, name='create_vacancy'),
    path("search/", views.SearchResultsView.as_view(), name="search_results")
]