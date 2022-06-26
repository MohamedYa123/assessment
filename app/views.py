
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect,reverse
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
import random as rd
import re

# Create your views here.
def Login(request):
    message=""
    if request.user.is_authenticated:
         #  print("DONENENJFDigbdfjgwekq")
           return  HttpResponseRedirect(reverse("home"))
    if request.method=="POST":
        user=authenticate(username=request.POST["username"],password=request.POST["Password"])
        if user!=None:
           login(request,user)
         #  print("DONENENJFDigbdfjgwekq")
           return  HttpResponseRedirect(reverse("home"))
        else:
            message="Invalid username or password"
    return render(request,template_name="Login.html" ,context={"msg":message})
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

def homepage(request):
    content_all=[]
    content_ans=[]
    if request.user.is_authenticated or True:
        if  request.user.is_authenticated :
            ac_ans=list( assumtion_to_ans.objects.filter(user=request.user))
            content_ans=ac_ans
        ac_asses=list(assessment.objects.all())
        content_all=ac_asses
    return render(request,template_name="home.html",context={"contenta":content_all,"contentans":content_ans})
def register(request):
    msg=""
    formg=selectgender()
    if not request.user.is_authenticated:
        #print('create1')
        if request.method=='POST':
         #   print('create2')
            j=assumtion_to_ans.objects.get(id=int(request.POST["idofassumt"]))
            email_k=request.POST['email']
            if not check(email_k):
                msg="invalid email"
                return render(request, template_name='register.html', context={"msg":msg,"formg":formg})
            else:
                pinfs=User.objects.filter(email=email_k)
                if len(pinfs)>0:
                    msg="email already used"
                    return render(request, template_name='register.html', context={"msg":msg,"formg":formg})
            if j.assessment_result<j.assessment_id.assessment_success or j.user!=None or j.assessment_id.assessment_index!=1:
                msg="invalid result"
                return render(request, template_name='register.html', context={"msg":msg,"formg":formg})
            if request.POST['password']==request.POST['confirm']:
               user=User.objects.create_user(request.POST['yourname'], request.POST['email'], request.POST['password'])
               user.is_active=False
               pr=profileinfo()
               pr.user=user
               pr.location=government.objects.get(id=1)
               pr.First_name=request.POST['firstn']
               pr.Last_name=request.POST['lastn']
               pr.gender=genders.objects.get(id=int(request.POST['gender']))
               j.user=user
               j.save()
               pr.save()
               user.save()
               acv=activation_form()
               acv.activation_string=str(rd.randrange(10**8,10**16))
               acv.user=user
               acv.save()
               email_body='Activate your Email here \r\n http://127.0.0.1:8000/activate/'+acv.activation_string
               send_mail(
                'Activate your email'
                ,email_body,
                settings.EMAIL_HOST_USER
                ,[request.POST['email']]
                ,fail_silently=False)


               return HttpResponseRedirect(reverse("login"))
            else:
                msg="password didn't match"
                return render(request, template_name='register.html', context={"msg":msg,"formg":formg})
            return HttpResponseRedirect(reverse('login'))
        else:
             return render(request,template_name='register.html',context={"msg":msg,"formg":formg})
    return HttpResponseRedirect(reverse("home"))
def editprofile(request):
    msg=""
    info=""
    form=""
    if request.user.is_authenticated:
        pr = profileinfo.objects.get(user=request.user)
        info=pr
        form=formimg()
        form2=profileinfof()
        if request.method=="POST":
            pr.First_name=request.POST['First_name']
            pr.Last_name=request.POST['Last_name']
            pr.About=str(request.POST['About'])
            pr.Age=int(request.POST['Age'])
            #pr.image=request.FILES['image']
            pr.location = government.objects.get(id=int(request.POST["location"]))
            pr.save()
            request.user.email=request.POST['email']
            request.user.save()
            msg="informations updated"
    return render(request,template_name="editprofile.html",context={"msg":msg,"info":info,"form":form,"form2":form2})
def uploadprofile(request):
    msg=""
    info=""
    form=""
    if request.user.is_authenticated:
        pr = profileinfo.objects.get(user=request.user)
        #info=pr
        form=formimg()
        #form2=profileinfof()
        if request.method=="POST":
            #pr.First_name=request.POST['firstn']
            #pr.Last_name=request.POST['lastn']
            #pr.About=str(request.POST['about'])
            pr.image=request.FILES['image']
            #pr.location = government.objects.get(id=int(request.POST["location"]))
            pr.save()
            #request.user.email=request.POST['email']
            #request.user.save()
            msg="informations updated"
            return  HttpResponseRedirect( reverse("profile",kwargs={"id":request.user.id}) )
    return render(request,template_name="uploadprofile.html",context={"msg":msg,"info":info,"form":form})

def profile(request,id):
    info=""
    e=False
    myuser=""
    #if request.user.is_authenticated:
    try:
        myuser=User.objects.get(id=id)
        pr = profileinfo.objects.get(user=myuser)
        info=pr
        if request.user.is_authenticated:
            if request.user.id==id:
                e=True
    except:
        []
    return render(request, template_name="profile.html", context={"info": info,"e":e,"myuser":myuser})
def viewanalytics(request,id):
    info=""
    e=False
    myuser=""
    #if request.user.is_authenticated:
    try:
        myuser=User.objects.get(id=id)
        pr = list(file.objects.filter(user=myuser))
        l=[]

        for k in pr:
            g=[k.filename(),k.text]
            l.append(g)
        info=l
        if request.user.is_authenticated:
            if request.user.id==id:
                e=True
    except:
        []
    return render(request, template_name="analytics.html", context={"info": info,"e":e,"myuser":myuser})
def view_assessment(request,id):
    asses=assessment.objects.filter(assessment_index=id)[0]
    qs=""
    arr=[]
    k=True
    if request.method!="POST":
        if asses.assessment_link!=-1 and request.user.is_authenticated :
                    aj=assessment.objects.filter(assessment_index=asses.assessment_link)[0]
                    j2= assumtion_to_ans.objects.filter(user=request.user,assessment_id=aj)
                    if len(j2)==0 or j2[0].assessment_result<j2[0].assessment_id.assessment_success:
                        k=False

        if not request.user.is_authenticated and id!=1:
            k=False
        #adding answer to all questions
        """
        for qj in question.objects.all():
            #1
            a=answers()
            a.question_id=qj
            a.ans_text="Practice is applied fully The organization has the practice and fully applied it currently."
            a.correct=True
            a.save()
            #2
            a=answers()
            a.question_id=qj
            a.ans_text=" Practice needs improvement The organization has the practice and fully applied it currently, but they want to modify/improve it based on their experience/circumstances."
            a.save()
            #3
            a=answers()
            a.question_id=qj
            a.ans_text="Practice is applied partially The organization has the practice and partially applied it currently"
            a.save()
            #4
            a=answers()
            a.question_id=qj
            a.ans_text="Practice is not practiced The organization does not know the practice (OR) The organization had never heard the practice (OR) The organization has not applied the practice currently (OR) The practice is not existing currently (available)."
            a.save()
         """   
        qs=question.objects.filter(assessment_id=asses)
        for q in qs:
            a=answers.objects.filter(question_id=q)
            s="<h1>"+q.text+"</h1><br>"
            s2=""#<form action="" , method='POST' >"
            for j in a:
                s2+=' <div class="form-check"><input class="form-check-input" type="radio" id="'+str(j.id) +'" value="'+str(j.id)+'" name="'+str(q.id)+'">'+'<label class="form-check-label" for="'+str(j.id)+'">'+str(j.ans_text)+'</label></div>'
            s2+=""#</form>"
            arr.append([s,s2])
    else:
        if request.user.is_authenticated or id==1:
            
            if request.user.is_authenticated:
                j= assumtion_to_ans.objects.filter(user=request.user,assessment_id=asses)
            elif id==1:
                j=[]
            else:
                return HttpResponseRedirect(reverse("home"))
            if (len(j)>0):
                j=j[0]
            elif id==1:
                j=assumtion_to_ans()
                if (request.user.is_authenticated):
                    j.user=request.user
            else:
                k=True
                if asses.assessment_link!=-1 and request.user.is_authenticated :
                    aj=assessment.objects.filter(assessment_index=asses.assessment_link)[0]
                    j2= assumtion_to_ans.objects.filter(user=request.user,assessment_id=aj)
                    if len(j2)==0:
                        k=False
                if not request.user.is_authenticated and id!=1:
                    k=false
                if not k:
                    return HttpResponseRedirect(reverse("home"))
                j=assumtion_to_ans()
                if (request.user.is_authenticated):
                    j.user=request.user
                #getting result
            result=0
            qs=question.objects.filter(assessment_id=asses)
            for q in qs:
                    a=answers.objects.filter(question_id=q)
                    l=list(request.POST)
                    for jj in a:
                        r=request.POST.get(str(q.id))
                        if r==str(jj.id):
                            r=True
                        else:
                            r=False
                        if jj.correct==r and jj.correct==True:
                            result+=1
            j.assessment_result=result
            j.assessment_id=asses
            j.save()
            return HttpResponseRedirect(reverse("result",args=(j.id,)))
        else :
            return HttpResponseRedirect(reverse("home"))
    return render(request, template_name="assessment.html", context={"asses":asses,"qs":arr,"k":k})
def view_result(request, id):
    a_t=assumtion_to_ans.objects.filter(id=id)[0]
    a2=a_t.assessment_id
    context={"a_t":a_t,"a2":a2}
    return render(request, template_name="result_view.html",context=context)
def activate_account(request,id):
    acvs=activation_form.objects.filter(activation_string=id)
    msg='<label style="color:red">Invalid activation url</label>'
    if (len(acvs)>0  ):#and acvs[0].user==request.user and request.user.is_authenticated
        acvs[0].user.is_active=True
        acvs[0].user.save()
        msg='<label style="color:green">Account activated</label>'
    return render(request, template_name="activate.html", context={"msg":msg})

 
def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False