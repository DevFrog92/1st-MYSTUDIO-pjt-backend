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
    path('review/<int:review_pk>/read_create_comment/', views.read_create_comment, name='read_create_comment'),
    path('review/<int:comment_pk>/delete_update_comment/', views.delete_update_comment, name='delete_update_comment'),
    path('<int:review_pk>/like/', views.like, name='like'),
    path('analyze_image/', views.analyze_image, name='analyze_image'),
    path('profile/',views.profile,name = 'profile'),
    path('updateprofile/',views.updateprofile,name = 'updateprofile'),

]
