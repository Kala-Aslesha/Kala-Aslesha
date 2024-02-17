from django.shortcuts import render,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User,auth
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Resume
import numpy as np
import pandas as pd
import requests
import nltk
import spacy 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn import metrics
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
driver_path = "C:\\Users\\Tejaswini Sista\\Desktop\\chromedriver.exe"
from bs4 import BeautifulSoup
from time import sleep
import csv
nlp = spacy.load("en_core_web_sm")
from pyresparser import ResumeParser
import os
from docx import Document
def home(request):
    return render(request,'calc/home.html')

def register(request):
    regForm=UserCreationForm
    if request.method=='POST':
        regForm=UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request,'user has been registered.')
            return redirect('login')
    return render(request,'registration/register.html',{"form":regForm})

def login(request):
    if request.method=='POST':
        form1=AuthenticationForm(data=request.POST)
        if form1.is_valid():
            return redirect('upload')
    else:
        form1=AuthenticationForm()
    return render(request,'registration/login.html',{'form':form1})
def upload_file(request):
    if request.method == 'POST':
        file2=request.FILES["file"]
        document=Resume.objects.create(resume=file2)
        document.save()
        file3=document.resume.name.split('/')[-1]
        filed='media/media/'+file3
        try:
            doc = Document()
            with open(filed, 'r') as file:
                doc.add_paragraph(file.read())
                doc.save("text.docx")
                data1 = ResumeParser('text.docx').get_extracted_data()
        except:
            data1 = ResumeParser(filed).get_extracted_data()
        resume=data1['skills']
        print(resume)
        skills=[]
        skills.append(' '.join(word for word in resume))
        data = pd.read_csv("media/media/Modified.csv")
        X_train,X_test,y_train,y_test = train_test_split(data.Combined,data.Title,test_size = 0.15,random_state = 0)
        tfidf_vectorizer=TfidfVectorizer(max_df=0.52)
        tfidf_train_2=tfidf_vectorizer.fit_transform(X_train)
        tfidf_test_2=tfidf_vectorizer.transform(X_test)
        pass_tf=PassiveAggressiveClassifier()
        pass_tf.fit(tfidf_train_2,y_train)
        pred=pass_tf.predict(tfidf_test_2)
        score=metrics.accuracy_score(y_test,pred)
        print(score)
        le = LabelEncoder()
        data["TitleUse"] = le.fit_transform(data.Title)
        test=tfidf_vectorizer.transform(skills)
        pred1=pass_tf.predict(test)[0]
        print(pred1)
        search_title=pred1
        ex = []
        wrong = []
        t=0
        try:
            print("index:" ,t)
            t+=1
            url="https://www.glassdoor.co.in/Job/"+search_title
            print(url)
            r=requests.get(url)
            print(r)
            soup = BeautifulSoup(r.content,"lxml")
            #print(soup)
            job=soup.find_all("a",{"class":"css-l2wjgv e1n63ojh0 jobLink"})
            salary=soup.find_all("span",{"class":"css-1xe2xww e1wijj242"})
            location=soup.find_all("span",{"class":"css-3g3psg pr-xxsm css-iii9i8 e1rrn5ka0"})
            data=[]
            for i in range(20):
                x = {
                    'title'     : job[i].text,
                    'url'       : job[i].get('href'),
                    'salary'    : salary[i].text,
                    'location'  : (location[i].text)
                     }
                data.append(x)
            print(data)
        except Exception as e:
            ex.append(e)
            wrong.append((search_title, url))
        return HttpResponse("Your file was uploaded!!!")
    else:
        return render(request, 'calc/upload.html')
    

      


def logout(request):
    return render(request,'registration/logout.html')



