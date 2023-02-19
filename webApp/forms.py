# myproject/forms.py
from django import forms
from allauth.account.forms import SignupForm
from .models import Address,Profile,Doctor,Patient,BlogPost,Appointment
#Appointment


USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

SPECIALTIES_CHOICES = [
    ('General Medicine', 'General Medicine'),
    ('Dentistry', 'Dentistry'),
    ('Ophthalmology', 'Ophthalmology'),
    ('Surgery', 'Surgery'),
    ('Pediatrics', 'Pediatrics'),
    ('Dermatology', 'Dermatology'),
    ('Neurology', 'Neurology'),
    ('Oncology', 'Oncology'),
    ('Gynecology', 'Gynecology'),
    ('Cardiology', 'Cardiology'),
    ('Psychiatry', 'Psychiatry'),
    ('Orthopedics', 'Orthopedics'),
]



STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra & Nagar Haveli', 'Dadra & Nagar Haveli'),
    ('Daman & Diu', 'Daman & Diu'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu & Kashmir', 'Jammu & Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Puducherry', 'Puducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttarakhand', 'Uttarakhand'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),
)

SPECIALITIES = [
    ('mental_health', 'Mental Health'),
    ('heart_disease', 'Heart Disease'),
    ('diabetes', 'Diabetes'),
    ('cancer', 'Cancer'),
    ('respiratory_disease', 'Respiratory Disease'),
    ('neurological_disorder', 'Neurological Disorder'),
    ('gastrointestinal_disorder', 'Gastrointestinal Disorder'),
    ('autoimmune_disease', 'Autoimmune Disease'),
    ('infectious_disease', 'Infectious Disease'),
    ('genetic_disorder', 'Genetic Disorder'),
    ('skin_condition', 'Skin Condition'),
    ('orthopedic_condition', 'Orthopedic Condition'),
    # Add more disease options here...
]




# class CustomSignUpForm(SignupForm):
#     # fields and methods
#     first_name = forms.CharField(max_length=30, label='First Name',widget=forms.TextInput(attrs={
#         'placeholder': 'subrat',}))
#     last_name = forms.CharField(max_length=30, label='Last Name',widget=forms.TextInput(attrs={
#         'placeholder': 'singh',}))
#     profile_pic = forms.ImageField(label='Profile Picture')
#     user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, label='User Type')
#     line1 = forms.CharField(label='Address',widget=forms.TextInput(attrs={
#         'placeholder': '58/6 A block Vikas nagar kanpur',}))
  
#     city = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
#         'placeholder': 'Kanpur',}))
#     state = forms.ChoiceField(choices=STATE_CHOICES, required=True)
#     # state = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
#     #     'placeholder': 'U.P',}))
#     pincode = forms.CharField(max_length=6,widget=forms.TextInput(attrs={
#         'placeholder': '201206',}))

    
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password != confirm_password:
#             raise forms.ValidationError(
#                 "Password and confirm password fields did not match."
#             )
    
#     def save(self, request):
#         user = super().save(request)
        
#         address = Address.objects.create(
#             user=user,
#             line1=self.cleaned_data['line1'],
#             city=self.cleaned_data['city'],
#             state=self.cleaned_data['state'],
#             pincode=self.cleaned_data['pincode']
#         )
#         profile = Profile.objects.create(
#             user=user,
#             profile_pic=self.cleaned_data['profile_pic'],
#             user_type=self.cleaned_data['user_type']
#         )
#         user.profile = profile
#         user.address = address
        
#         if profile.user_type == "doctor":
#             doctor = Doctor.objects.create(user=user)
#             user.doctor = doctor
#         elif profile.user_type == "patient":
#             patient = Patient.objects.create(user=user)
#             user.patient = patient
        
#         user.save()
#         return user




class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'image', 'category', 'summary', 'content', 'is_draft')
        labels = {
            'title': 'Title',
            'image': 'Image',
            'category': 'Category',
            'summary': 'Summary',
            'content': 'Content',
            'is_draft': 'Draft'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'is_draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }




class DraftStatusForm(forms.ModelForm):
    DRAFT_CHOICES = (
        (True, 'Draft'),
        (False, 'Published'),
    )
    draft = forms.TypedChoiceField(
        label='Draft status',
        choices=DRAFT_CHOICES,
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
    )

    class Meta:
        model = BlogPost
        fields = ['draft']




class DoctorSpecialityForm(forms.ModelForm):
    speciality = forms.TypedChoiceField(choices=SPECIALTIES_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Doctor
        fields = ['speciality']


class AppointmentForm(forms.ModelForm):
    speciality = forms.TypedChoiceField(choices=SPECIALITIES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Appointment
        fields = ['speciality', 'date', 'start_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class CustomSignUpForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name',widget=forms.TextInput(attrs={
        'placeholder': 'subrat',}))
    last_name = forms.CharField(max_length=30, label='Last Name',widget=forms.TextInput(attrs={
        'placeholder': 'singh',}))
    profile_pic = forms.ImageField(label='Profile Picture',required=False)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, label='User Type')
    line1 = forms.CharField(label='Address',widget=forms.TextInput(attrs={
        'placeholder': '58/6 A block Vikas nagar kanpur',}))
  
    city = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'placeholder': 'Kanpur',}))
    state = forms.TypedChoiceField(choices=STATE_CHOICES ,label='State')
    pincode = forms.CharField(max_length=6,widget=forms.TextInput(attrs={
        'placeholder': '201206',}))

    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and confirm password fields did not match."
            )
    
    def save(self, request):
        user = super(CustomSignUpForm,self).save(request)
        address = Address.objects.create(user=user,line1=self.cleaned_data['line1'], city=self.cleaned_data['city'], state=self.cleaned_data['state'], pincode=self.cleaned_data['pincode'])
      
        profile = Profile.objects.create(user=user, profile_pic=self.cleaned_data['profile_pic'], user_type=self.cleaned_data['user_type'])
        user.profile = profile
        user.address = address
        if profile.user_type == "doctor":
            doctor=Doctor.objects.create(user=user)
            user.doctor = doctor
        elif profile.user_type == "patient":
            patient = Patient.objects.create(user=user)
            user.patient = patient
        user.save()
        return user
