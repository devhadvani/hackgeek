from django.contrib import admin
from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('register/' , views.register , name='register'),
    path('log',views.log, name='log'),
    path('',views.home, name='home'),
    path('logout_form/' , views.logout_form , name='logout_form'),
    path('host_hack/' , views.host_hack , name='host_hack'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit_file/<int:id>', views.edit_file, name='edit_file'),
    path('participants_data', views.participants_data, name='participants_data'),
    path('hack_details/<int:pk>', views.hack_details, name='hack_details'),
    path('apply/<int:id>', views.apply, name='apply'),
    path('part_details/<int:id>', views.part_details, name='part_details'),
    path('store_file/', views.store_file, name='store_file'),
    path('create_winner/<int:id>', views.create_winner, name='create_winner'),
    path('clear_winners/<int:id>', views.clear_winners, name='clear_winners'),
    path('winner_results/<int:project_id>', views.winner_results, name='winner_results'),
    path('check_email_availability/', views.check_email_availability, name='check_email_availability'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
+ static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)