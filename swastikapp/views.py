import math
import pandas as pd
from django.shortcuts import redirect, render
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier






from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required


from django.conf import settings
from django.core.mail import send_mail

#Registering Users

from .forms import NewUserForm
from django.shortcuts import  render, redirect ,HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


@login_required(login_url='login')
def disease(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def appointment(request):
    return render(request, 'appointment.html')


@login_required(login_url='login')
def predict(request):
    return render(request, 'predict.html')


def doctor(request):
    return render(request, 'doctor.html')

@login_required(login_url='login')
def appointment_result(request):
    your_name = request.POST['your_name']
    your_phone = request.POST['your_phone']
    your_address = request.POST['your_address']
    your_email = request.POST['your_email']
    appointment_day = request.POST['appointment_day']
    appointment_time = request.POST['appointment_time']
    your_doctor = request.POST['your_doctor']
    your_message = request.POST['your_message']
 
    email_message = "Patient name: " + your_name + " Patient Phone number: " + your_phone + " Appointment day: " + appointment_day + " Appointment Time: " + appointment_time + " Patient's Remarks: " + your_message
    
    send_mail(
        your_name,
        email_message,
        your_email,
        ['sabinprajapati7@gmail.com']
    )
    return render(request, 'appointment_result.html', {
        'your_name': your_name,
        'your_phone': your_phone, 
        'your_address': your_address,
        'your_email' : your_email,
        'appointment_day' : appointment_day,
        'appointment_time' : appointment_time,
        'your_doctor' : your_doctor,
        'your_message' : your_message
        })
        



def home(request):
    return render(request, 'home.html')

@unauthenticated_user
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
   
			messages.success(request, "Registration successful for " )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

@unauthenticated_user
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
        logout(request)
        messages.info(request, "You have successfully logged out.") 
        return redirect('home')
    

def predict(request):
    if request.method == 'POST':
        temp = {}
        temp['rashness'] = request.POST.get('rashness')
        temp['swellingeyes'] = request.POST.get('swellingeyes')
        temp['diarrhea'] = request.POST.get('diarrhea')
        temp['dehydration'] = request.POST.get('dehydration')
        temp['pressure'] = request.POST.get('pressure')
        temp['fever'] = request.POST.get('fever')
        temp['headache'] = request.POST.get('headache')
        temp['vomiting'] = request.POST.get('vomiting')
        temp['muscleache'] = request.POST.get('muscleache')
        temp['sweat'] = request.POST.get('sweat')
        temp['scalyskin'] = request.POST.get('scalyskin')
        temp['cough'] = request.POST.get('cough')
        temp['enlargementofliver'] = request.POST.get('enlargementofliver')


        data = pd.read_csv('./model/dataset.csv')

        features = ['Rashness','Swelling_Eyes','Diarrhea','Dehydration','Blood_Pressure','Fever', 'Headache', 'Vomiting', 'Muscle_Aches','Night_Sweats','Scaly_skin','Cough', 'Enlargement_of_Liver']
        target = ['Diseases']
        df = data.fillna(method='ffill')
        X = df[features]
        y = df[target]


        le = LabelEncoder()
        X_encoding = X.apply(le.fit_transform)
        x = X_encoding.values

        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=2, random_state=1)

        model = DecisionTreeClassifier()
        clf_dt=model.fit(x, y)

        inputs = [temp['rashness'], temp['swellingeyes'], temp['diarrhea'],
                  temp['dehydration'],temp['pressure'],temp['fever'],
                  temp['headache'],temp['vomiting'], temp['muscleache'],
                  temp['sweat'],temp['scalyskin'], temp['cough'],temp['enlargementofliver']]
        
        symptoms_encoding = le.fit_transform(inputs)
        updated_encoding = symptoms_encoding.reshape(1,-1)
        
        Disease = clf_dt.predict(updated_encoding)
        
        
        if Disease == 'Malaria':
            PredictedDisease = "Malaria"
            Medicine = "and the recommended medicine is Hydroxychloroquine Sulfate Tablets, USP"
        elif(Disease == 'Kala zar'):
            PredictedDisease = 'KalaZar'
            Medicine = " KalaZar and the recommended medicine is REPL Dr. Advice No 106 (Kala Azar) (30ml)"
        elif(Disease == 'Measles'):
            PredictedDisease = 'Measles'
            Medicine = "  and the recommended medicine is Medicine Grade Measles Vaccine"
        else:
            PredictedDisease = 'Cholera'
            Medicine = " and the recommended medicine is Sanchol"

        return render(request, 'result.html', {'Disease': PredictedDisease, 'Medicine':  Medicine})


from .models import Doctors

def get_data(request):
    data = Doctors.objects.all()
    return render(request, 'doctor.html', {'data': data})

def appointment_data(request):
    datas = Doctors.objects.all()
    return render(request, 'appointment.html', {'datas': datas})



