import json

import numpy as np
import pandas as pd
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from predictionapp.models import *
from predictionapp.nb import MultinomialNB
# import numpy as np



# from sklearn.model_selection import train_test_split
# from sklearn import datasets
# # import matplotlib.pyplot as plt





# Create your views here.
def home(request):
    if request.user.is_staff:
        return redirect('admindashboard')
    return render(request, 'home.html')
def homee(request):
    if request.user.is_staff:
        return redirect('admindashboard')
    return render(request, 'home1.html')


def index(request):
    return render(request, 'navigation.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contactus.html')


def adminLogin(request):
    # msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login successfully")
                # msg = "User login successfully"
                return redirect('admindashboard')
            else:
                messages.success(request, "Invalid Credentials")
                # msg = "Invalid Credentials"
        except:
            messages.success(request, "Invalid Credentials")
    # dic = {'msg': msg}
    # return render(request, 'admin_login.html', dic)
    return render(request, 'admin_login.html')


def adminHome(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    return render(request, 'admin_base.html')


def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    user = UserProfile.objects.filter()
    doctor = Adddoctor.objects.filter()

    disease = diseaseinfo.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    approved_blood = Blood.objects.filter(status=1)
    deny_blood = Blood.objects.filter(status=2)
    return render(request, 'admin_dashboard.html', locals())


def add_doctor(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    if request.method == "POST":
        name = request.POST['name']
        speciality = request.POST['speciality']
        fee = request.POST['fee']
        image = request.FILES['image']
        desc = request.POST['desc']

        Adddoctor.objects.create(name=name, speciality=speciality, fee=fee, image=image, description=desc)
        messages.success(request, "Doctor added")
        # msg = "Doctor added"
        return redirect('view_doctors')
    return render(request, 'add_doctor.html', locals())


def view_doctors(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    doctor = Adddoctor.objects.all()
    return render(request, 'view_doctors.html', locals())


def edit_doctor(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    doctor = Adddoctor.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']

        speciality = request.POST['speciality']
        fee = request.POST['fee']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            doctor.image = image
            doctor.save()
        except:
            pass
        Adddoctor.objects.filter(id=pid).update(name=name, speciality=speciality, fee=fee, description=desc)

        messages.success(request, "Doctor updated")
        return redirect('view_doctors')
        # msg = "Doctor Updated"
    return render(request, 'edit_doctor.html', locals())


def delete_doctor(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    doctor = Adddoctor.objects.get(id=pid)
    doctor.delete()
    messages.success(request, "Doctor Deleted")
    return redirect('view_doctors')


def registration(request):

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email,
                                        password=password)
        UserProfile.objects.create(user=user, mobile=mobile, address=address)
        messages.success(request, "Registration Successful")
    return render(request, 'registration.html', locals())


def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.success(request, "Invalid Credentials")
    return render(request, 'login.html', locals())

def profile(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user = User.objects.get(id=request.user.id)
    data = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        UserProfile.objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile updated")
        return redirect('profile')
    return render(request, 'profile.html', locals())


def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('homee')

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('home')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')

def user_feedback(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        Feedback.objects.create(user=request.user, message=request.POST['feedback'])
        messages.success(request, "Feedback sent successfully")
    return render(request, "feedback-form.html", locals())


def manage_feedback(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'manage_feedback.html', locals())

def delete_feedback(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('manage_feedback')

def read_feedback(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")


def manage_user(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    user = UserProfile.objects.all()
    return render(request, 'manage_user.html', locals())

def view_search(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    history = diseaseinfo.objects.all()
    return render(request, 'view_search.html', locals())

def delete_user(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_user')


def admin_change_password(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('admin_login')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')

def register_for_blood_donation(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        Blood.objects.create(user=request.user, bloodgroup=request.POST['bloodgroup'],mobilenumber=request.POST['mobile'], address=request.POST['address'])
        messages.success(request, "Blood Donation Register Request Sent Successfully")
    return render(request, "register_for_blood_donation.html", locals())

def view_blood_donor(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    action = request.GET.get('action', 1)
    blood = Blood.objects.filter(status=int(action))
    if 'q' in request.GET:
        q= request.GET['q']
        # blood=Blood.objects.filter(Q(address__icontains=q) | Q(bloodgroup__exact=q))
        blood = Blood.objects.filter(Q(address__icontains=q))
    return render(request, 'view_blood_donator.html', {'blood':blood})

def manage_blood(request):
    action = request.GET.get('action', 0)
    blood = Blood.objects.filter(status=int(action))
    return render(request, 'manage_blood.html', locals())

def delete_blood(request, pid):
    blood = Blood.objects.get(id=pid)
    blood.delete()
    messages.success(request, "Deleted successfully")
    return redirect('manage_blood')

def read_blood(request, pid):
    blood = Blood.objects.get(id=pid)
    blood.status = 1
    blood.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")
def unread_blood(request, pid):
    blood = Blood.objects.get(id=pid)
    blood.status = 2
    blood.save()
    return HttpResponse(json.dumps({'id':2, 'status':'success'}), content_type="application/json")

def add_donor(request):
    if request.method == "POST":
        nam = request.POST['nam']
        male = request.POST['male']
        bloodgroup = request.POST['bloodgroup']
        mobile = request.POST['mob']
        address = request.POST['address']
        Blood.objects.create(nam=nam, male=male, bloodgroup=bloodgroup, mobilenumber=mobile, address=address)
        msg = "Donor added"
    return render(request, 'add_blood_donor.html', locals())

def checkdisease(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')

    disease= ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer diseae',
                  'AIDS', 'Diabetes ',
                  'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'Cervical spondylosis',
                  'Paralysis (brain hemorrhage)',
                  'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B',
                  'Hepatitis C', 'Hepatitis D',
                  'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
                  'Dimorphic hemmorhoids(piles)',
                  'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
                  'Osteoarthristis',
                  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection',
                  'Psoriasis', 'Impetigo']

    l1 = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
                    'joint_pain',
                    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
                     'spotting_ urination',
                    'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss',
                    'restlessness', 'lethargy',
                    'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes',
                    'breathlessness', 'sweating',
                    'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
                    'loss_of_appetite', 'pain_behind_the_eyes',
                    'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
                    'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
                    'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
                    'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                    'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                    'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                    'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                    'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                    'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
                    'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                    'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
                    'belly_pain',
                    'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite',
                    'polyuria', 'family_history', 'mucoid_sputum',
                    'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
                    'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
                    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
                    'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
                    'red_sore_around_nose',
                    'yellow_crust_ooze']

    alphabaticsymptomslist = sorted(l1)





    from sklearn.naive_bayes import MultinomialNB






    if request.method == 'GET':
        return render(request, 'checkdisease.html', {"list2": alphabaticsymptomslist})
    if request.method == "POST":
            psymptoms = []
            psymptoms = request.POST.getlist("symptoms[]")
            array_length = len(psymptoms)

            # print(psymptoms)

            """      #main code start from here...
            """

            l2 = []
            # append zero in all coloumn fields...
            for x in range(0, len(l1)):
                l2.append(0)

            # TESTING DATA
            tr = pd.read_csv("Testing.csv")
            tr.replace({'prognosis': {'Fungal infection': 0, 'Allergy': 1, 'GERD': 2, 'Chronic cholestasis': 3,
                                      'Drug Reaction': 4,
                                      'Peptic ulcer diseae': 5, 'AIDS': 6, 'Diabetes ': 7, 'Gastroenteritis': 8,
                                      'Bronchial Asthma': 9, 'Hypertension ': 10,
                                      'Migraine': 11, 'Cervical spondylosis': 12,
                                      'Paralysis (brain hemorrhage)': 13, 'Jaundice': 14, 'Malaria': 15,
                                      'Chicken pox': 16, 'Dengue': 17, 'Typhoid': 18, 'hepatitis A': 19,
                                      'Hepatitis B': 20, 'Hepatitis C': 21, 'Hepatitis D': 22, 'Hepatitis E': 23,
                                      'Alcoholic hepatitis': 24, 'Tuberculosis': 25,
                                      'Common Cold': 26, 'Pneumonia': 27, 'Dimorphic hemmorhoids(piles)': 28,
                                      'Heart attack': 29, 'Varicose veins': 30, 'Hypothyroidism': 31,
                                      'Hyperthyroidism': 32, 'Hypoglycemia': 33, 'Osteoarthristis': 34, 'Arthritis': 35,
                                      '(vertigo) Paroymsal  Positional Vertigo': 36, 'Acne': 37,
                                      'Urinary tract infection': 38, 'Psoriasis': 39,
                                      'Impetigo': 40}}, inplace=True)

            X_test = tr[l1]
            y_test = tr[["prognosis"]]
            print(y_test)
            np.ravel(y_test)


            # TRAINING DATA
            df = pd.read_csv("Training.csv")

            df.replace({'prognosis': {'Fungal infection': 0, 'Allergy': 1, 'GERD': 2, 'Chronic cholestasis': 3,
                                      'Drug Reaction': 4,
                                      'Peptic ulcer diseae': 5, 'AIDS': 6, 'Diabetes ': 7, 'Gastroenteritis': 8,
                                      'Bronchial Asthma': 9, 'Hypertension ': 10,
                                      'Migraine': 11, 'Cervical spondylosis': 12,
                                      'Paralysis (brain hemorrhage)': 13, 'Jaundice': 14, 'Malaria': 15,
                                      'Chicken pox': 16, 'Dengue': 17, 'Typhoid': 18, 'hepatitis A': 19,
                                      'Hepatitis B': 20, 'Hepatitis C': 21, 'Hepatitis D': 22, 'Hepatitis E': 23,
                                      'Alcoholic hepatitis': 24, 'Tuberculosis': 25,
                                      'Common Cold': 26, 'Pneumonia': 27, 'Dimorphic hemmorhoids(piles)': 28,
                                      'Heart attack': 29, 'Varicose veins': 30, 'Hypothyroidism': 31,
                                      'Hyperthyroidism': 32, 'Hypoglycemia': 33, 'Osteoarthristis': 34, 'Arthritis': 35,
                                      '(vertigo) Paroymsal  Positional Vertigo': 36, 'Acne': 37,
                                      'Urinary tract infection': 38, 'Psoriasis': 39,
                                      'Impetigo': 40}}, inplace=True)

            X = df[l1]

            y = df[["prognosis"]]
            np.ravel(y)


            # from sklearn.metrics import confusion_matrix



            # from predictionapp.nb import NaiveBayes
            gnb = MultinomialNB()
            # gnb = NaiveBayes()
            gnb = gnb.fit(X, np.ravel(y))
            from sklearn.metrics import accuracy_score
            # from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix
            y_pred = gnb.predict(X_test)
            # print(y_pred)
            # print(accuracy_score(y_test, y_pred))
            # cm = confusion_matrix(y_test, y_pred)

            # def confusion_matrix_to_2x2(conf_matrix):
            #     tp = conf_matrix[0][0]
            #     tn = np.sum(conf_matrix) - np.sum(conf_matrix[0]) - np.sum(conf_matrix[:, 0]) + tp
            #     fp = np.sum(conf_matrix[:, 0]) - tp
            #     fn = np.sum(conf_matrix[0]) - tp
            #     return np.array([[tp, fp], [fn, tn]])

            # print(confusion_matrix_to_2x2(cm))
            confidencescore=accuracy_score(y_test, y_pred, normalize=False)
            # print(confidencescore)




            # update 1 where symptoms gets matched...
            for k in range(0, len(l1)):
                for z in psymptoms:
                    if (z == l1[k]):
                        l2[k] = 1

            inputtest = [l2]
            predict = gnb.predict(inputtest)
            predicted = predict[0]
            # predicted_array = np.array([predicted])
            # print (predicted_array)


            h = 'no'
            for a in range(0, len(disease)):
                if (disease[predicted] == disease[a]):
                    h = 'yes'
                    break

            if (h == 'yes'):
                print(disease[a])

                new_disease_info = diseaseinfo()
                # assign values to the fields of the new instance
                new_disease_info.user = request.user  # or assign some user object directly
                new_disease_info.diseasename = disease[a]
                new_disease_info.no_of_symp = array_length
                new_disease_info.symptomsname = psymptoms
                new_disease_info.confidence = confidencescore

                # save the new instance to the database
                new_disease_info.save()







        # return HttpResponse('You may have ' + disease[a])
        #     messages.success(request, "You may have {} and Confidence Score: {}".format(disease[a], confidencescore))
            messages.success(request, "Disease might be {}".format(disease[a]))
            return render(request, "checkdisease.html",{"list2": alphabaticsymptomslist})

def predicteddisease(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    return render(request, "predicteddisease.html")
def showhistory(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user = request.user
    history = diseaseinfo.objects.filter(user=user)
    context = {'history': history}
    return render(request, 'showhistory.html', context)

