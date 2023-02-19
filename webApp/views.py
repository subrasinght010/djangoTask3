from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView,UpdateView,DetailView
from .models import BlogPost,Doctor,Profile
from django.conf import settings
from django.http import HttpResponse

from django.core.paginator import Paginator
from .calenders import create_calendar_event
from .forms import BlogPostForm,DraftStatusForm,DoctorSpecialityForm,AppointmentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta,time

class HomeView(TemplateView):
    template_name = "webApp/home.html"


@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('webApp:blog_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'webApp/create_blog_post.html', {'form': form})




@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('webApp:blog_list')




class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'webApp/post_detail.html'
    context_object_name = 'post'


@login_required
def dashboard(request):
    profile = request.user.profile 
    user_type = profile.user_type
    
    if user_type == "patient":
        return redirect('webApp:patient_dashboard')
    elif user_type == "doctor":
        return redirect('webApp:doctor_dashboard')
    else:
        return HttpResponse("Unknown user type")





def patient_dashboard(request):
    return render(request, 'webApp/patient_dashboard.html')


@login_required
def doctor_dashboard(request):
    doctor = request.user.doctor
    speciality = doctor.speciality
    
    if speciality:
        has_speciality = False
    else:
        has_speciality = True
    
    
    context = {
        
        'has_speciality': has_speciality,}
    
    return render(request, 'webApp/doctor_dashboard.html', context)



class DoctorBlogListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'webApp/doctor_dashboard.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            messages.success(request, 'Your post was created successfully!')
            return redirect('webApp:blog_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'webApp/create_blog_post.html', {'form': form})



class BlogUpdateView(UpdateView):
    model = BlogPost
    template_name = 'webApp/create_blog_post.html'
    form_class = BlogPostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.created_by = self.request.user
        post.save()
        messages.success(self.request, 'Your post was updated successfully!')
        return redirect('webApp:blog_detail', pk=post.pk)    










    
def change_draft_status(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = DraftStatusForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.draft = form.cleaned_data['draft']
            post.save()
            return redirect('webApp:doctor_dashboard')
    else:
        form = DraftStatusForm(instance=post)
    return render(request, 'webApp/draft_status.html', {'form': form})





class DoctorListView(ListView):
    model = Doctor
    template_name = 'webApp/doctorlist.html'
    context_object_name = 'doctors'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctors = self.get_queryset()
        paginator = Paginator(doctors, self.paginate_by)
        page = self.request.GET.get('page')
        doctors = paginator.get_page(page)
        context['doctors'] = doctors
        return context





class BlogPostListView(ListView):
    model = BlogPost
    paginate_by = 2
    template_name = 'webApp/post_list.html'
    context_object_name = 'posts'
    queryset = BlogPost.objects.filter(is_draft=False)

# class BlogPostListView(LoginRequiredMixin, ListView):
#     model = BlogPost
#     template_name = 'webApp/post_list.html'
#     context_object_name = 'posts'
#     ordering = ['-created_at']
#     paginate_by = 4  # Number of posts to display per page

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(created_by=self.request.user)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         posts = context['object_list']
#         paginator = Paginator(posts, self.paginate_by)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         context['page_obj'] = page_obj
#         return context



@login_required
def update_doctor_speciality(request):
    doctor = request.user.doctor
    if doctor.speciality:
        return redirect('webApp:doctor_dashboard')
    
    if request.method == 'POST':
        form = DoctorSpecialityForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your speciality has been updated successfully!')
            return redirect('webApp:doctor_dashboard')
    else:
        form = DoctorSpecialityForm(instance=doctor)
    return render(request, 'webApp/update_doctor_speciality.html', {'form': form})







def book_appointment(request,pk):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            total_minutes = appointment.start_time.hour * 60 + appointment.start_time.minute + 45
            appointment.end_time =str(timedelta(minutes=total_minutes))

            # Check if appointment is scheduled before 6pm closing time
            closing_time = time(hour=18, minute=0)
            appointment_time = time(hour=total_minutes//60,minute=total_minutes%60)
            if appointment_time > closing_time:
                messages.error(request, 'Appointments cannot be scheduled after 6pm')
                context = {'form': form}
                return render(request, 'webApp/book_appointment.html', context)

            appointment.doctor= Doctor.objects.get(pk=pk)
            appointment.save()
            t=appointment.start_time.hour * 60 + appointment.start_time.minute

            doctor = appointment.doctor
            appointment_time1 = time(hour=t//60,minute=t%60)

            start_time = appointment_time1
            delta = timedelta(minutes=45)

            start_datetime = datetime.combine(datetime.today(), start_time)  # Convert time object to datetime object
            end_datetime = start_datetime + delta
            end_time = end_datetime.time()

            try:
                # res= create_calendar_event(doctor, date, start_time)
                messages.success(request, 'Appointment booked successfully!')
                context = {
                'description': 'Appointment with Dr. ' + doctor.user.first_name + ' ' + doctor.user.last_name,
                'date' :appointment.date,
                'start' :appointment.start_time,
                'end':end_time,
                }
                return render(request, 'webApp/appointment_confirmation.html', context)
            except HttpError as error:
                messages.error(request, 'Error occurred while creating calendar event: ' + str(error))

    else:
        form = AppointmentForm()

    context = {'form': form}
    return render(request, 'webApp/book_appointment.html', context)


