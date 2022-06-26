from django.db import models
from django.conf import settings
import  os
# Create your models here.
class genders(models.Model):
    text=models.CharField(max_length=100)
    def __str__(self):
        return self.text
class government(models.Model):
    text=models.CharField(max_length=100)
    def __str__(self):
        return self.textgi
class profileinfo(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    First_name=models.CharField(default="",max_length=100)
    Last_name=models.CharField(default="",max_length=100)
    About = models.TextField(default="")
    image=models.ImageField(default="user.png")
    location = models.ForeignKey(government, on_delete=models.CASCADE,default=1)
    gender = models.ForeignKey(genders, on_delete=models.CASCADE,default=1)
    Age=models.IntegerField(default=18)
class file(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    myfile=models.FileField(default="")
    text=models.CharField(max_length=100)
    def filename(self):
        return os.path.basename(self.myfile.name)
    def __str__(self):
        return  self.text
class assessment(models.Model):
    assessment_name=models.CharField(max_length=1000)
    assessment_link=models.IntegerField()
    assessment_index=models.IntegerField()
    assessment_success=models.IntegerField()
    def __str__(self):
        return str(self.assessment_index)+" "+ self.assessment_name
class question(models.Model):
    assessment_id= models.ForeignKey(assessment, on_delete=models.CASCADE)
    text=models.CharField(max_length=1000)
    def __str__(self):
        return str(self.assessment_id)+" : "+ self.text
class answers(models.Model):
    question_id=models.ForeignKey(question,on_delete=models.CASCADE)
    ans_text=models.CharField(max_length=1000)
    checked=models.BooleanField(default=False)
    correct=models.BooleanField(default=False)
    def __str__(self) :
        return str(self.question_id)+" : "+ self.ans_text
class assumtion_to_ans(models.Model):
    assessment_id= models.ForeignKey(assessment, on_delete=models.CASCADE)
    assessment_result=models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True, on_delete=models.CASCADE)
class question_to_ans(models.Model):
    assessment_id=models.ForeignKey(assumtion_to_ans,on_delete=models.CASCADE)
class answer_to_ans(models.Model):
    question_id=models.ForeignKey(question_to_ans,on_delete=models.CASCADE)
class activation_form(models.Model):
    activation_string=models.CharField(max_length=1000)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True, on_delete=models.CASCADE)
    used=models.BooleanField(default=False)

