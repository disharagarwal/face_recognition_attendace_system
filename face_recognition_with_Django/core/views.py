import imp
from tracemalloc import start
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from requests import request
from .models import * 
from .forms import *
import face_recognition #face recognition library from python
import cv2 # helps to understand the content of the digital images such as photographs and videos
import numpy as np #for array computing
import winsound #to generate the beep sound 
from django.db.models import Q #Q object encapsulates a SQL expression in a Python object that can be used in database-related operations
import os
import time
import pandas as pd

last_face = 'no_face' 
current_path = os.path.dirname(__file__)  #path of the current folder 
sound_folder = os.path.join(current_path, 'sound/') #for the beep sound 
face_list_file = os.path.join(current_path, 'face_list.txt')
sound = os.path.join(sound_folder, 'beep.wav')


def index(request):
    scanned = LastFace.objects.all().order_by('date').reverse()  #all the profiles created in order of older to new
    present = Profile.objects.filter(present=True).order_by('updated').reverse() #checking who all are present 
    absent = Profile.objects.filter(present=False).order_by('shift') #checking who all are absent 
    context = {
        'scanned': scanned,
        'present': present,
        'absent': absent,
    }
    return render(request, 'core/index.html', context) #rendering the data to html file for the display


def ajax(request):
    last_face = LastFace.objects.last()
    context = {
        'last_face': last_face
    }
    return render(request, 'core/ajax.html', context)


def scan(request):

    global last_face

    known_face_encodings = []  #stores all the encoding of face form the images
    known_face_names = [] #stores all the profile name 

    profiles = Profile.objects.all()
    for profile in profiles:
        person = profile.image
        image_of_person = face_recognition.load_image_file(f'media/{person}')
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(f'{person}'[:-4])

#the above code loads each person from the profile calculate the face encoding and store it in known face encoding

    video_capture = cv2.VideoCapture(0)  #opens the window to capture the video 

    face_locations = []  
    face_encodings = []
    face_names = []
    #to calculate the face encodings of the person
    process_this_frame = True
    start_time=time.time()
    while True:

        ret, frame = video_capture.read()  #reading wile capturing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  #resizing the image size to the required dimensions
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:  #if their is face then calculate the face encodings
            face_locations = face_recognition.face_locations(rgb_small_frame) 
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []  
            for face_encoding in face_encodings: #comparing face with the face encodings calculated above  
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding) #comparing with the face distances 
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:  #if match is present 
                    name = known_face_names[best_match_index]  #then find the name from known face encodings

                    profile = Profile.objects.get(Q(image__icontains=name))
                    if profile.present == True: #if the person is already present then pass 
                        pass   
                    else:
                        profile.present = True #else mark the person as present 
                        profile.save()

                    if last_face != name: #if the last scanned person is not same then save the details 
                        last_face = LastFace(last_face=name)
                        last_face.save()
                        last_face = name
                        winsound.PlaySound(sound, winsound.SND_ASYNC)
                    else:
                        pass

                face_names.append(name)

        process_this_frame = not process_this_frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        end_time=time.time() #to close the capturing window in 10 seconds
        elapsed=end_time-start_time 
        if elapsed>10:
                break

    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponse('scaner closed', last_face)


def profiles(request):  #this functions returns all the profiles to the html page specified
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'core/profiles.html', context)


def details(request):
    try:
        last_face = LastFace.objects.last()  #when face recognized to show details about the person
        profile = Profile.objects.get(Q(image__icontains=last_face))
    except:
        last_face = None
        profile = None

    context = {
        'profile': profile,
        'last_face': last_face
    }
    return render(request, 'core/details.html', context)


def add_profile(request): #to create a new profile 
    form = ProfileForm
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profiles')
    context={'form':form}
    return render(request,'core/add_profile.html',context)


def edit_profile(request,id):  #to edit the details of the profile already present 
    profile = Profile.objects.get(id=id)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':  #for forms it is safe to use post 
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles')
    context={'form':form}
    return render(request,'core/add_profile.html',context)


def delete_profile(request,id):  #to remove the profile of a perticular person
    profile = Profile.objects.get(id=id)
    profile.delete()
    return redirect('profiles')


def clear_history(request):  #to clear all the history present till date 
    history = LastFace.objects.all()
    history.delete()
    return redirect('index')


def reset(request):  #this is the function to reset the details of all people present to mark absent on perticular day
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.present == True:
            profile.present = False
            profile.save()
        else:
            pass
    return redirect('index')



def Export_Excel(request):
    objs=LastFace.objects.all()
    data =[]
    for obj in objs:
        data.append({
            "name":obj.last_face,
            "date":obj.date,
        })

    pd.DataFrame(data).to_excel('Attendance.xlsx')
    return JsonResponse({
        'status' :200
    })



   
