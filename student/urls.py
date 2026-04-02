from django.urls import path
from .views import index,index2,add_student,user_signup,student_delete,login_user,student_edit,index0,export_csv


urlpatterns = [
   path('home/<int:pk>', index, name='home'),
   path('home2/', index2, name='home2'),
   path('add-student/',add_student,name='add-student'),
   path('signup/',user_signup,name='signup'),
   path('delete-student/<int:pk>',student_delete,name='delete'),
   path('',login_user,name='login'),
   path('edit/<int:pk>',student_edit,name='edit'),
   path('admin-dashboard/', index0, name='home0'),
   path('export/', export_csv, name='export_csv')
    
]