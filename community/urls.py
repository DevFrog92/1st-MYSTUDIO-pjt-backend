from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.review_read_create),
    path('<int:review_id>/', views.review_update_delete),
    # path('review/create/', views.create, name='create'),
    path('<int:review_pk>/update/', views.update, name='update'),
    path('<int:review_pk>/delete/', views.delete, name='delete'),
    path('review/<int:review_pk>/', views.detail, name='detail'),
    path('review/<int:review_pk>/comments/', views.create_comment, name='create_comment'),
    path('review/<int:review_pk>/like/', views.like, name='like'),
    path('analyze_image/', views.analyze_image, name='analyze_image'),
]
