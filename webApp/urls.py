from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DoctorListView,HomeView,BlogPostDetailView,DoctorBlogListView,BlogPostListView,book_appointment,update_doctor_speciality, patient_dashboard,BlogUpdateView,change_draft_status,dashboard,delete_post,create_post,BlogPostListView

app_name = 'webApp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    #path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path("dashboard/", dashboard, name="dashboard"),
    path("patient_dashboard/", patient_dashboard, name="patient_dashboard"),
    path('doctor/dashboard/', DoctorBlogListView.as_view(), name='doctor_dashboard'),
    path('posts/',BlogPostListView.as_view(), name='blog_list'),
    path('detail/<int:pk>/', BlogPostDetailView.as_view(), name='blog_detail'),
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('create/', create_post , name='blog_create'),
    path('updatespeciality/',update_doctor_speciality ,name='add_speciality' ),
    path('tag_update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('book_appointment/<int:pk>/', book_appointment, name='book_appointment'),
    path('delete/<int:pk>/', delete_post, name='blog_delete'),
    path('change/draft/<int:pk>' , change_draft_status ,name = 'change_draft')
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)