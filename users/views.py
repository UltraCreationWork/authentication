from django.shortcuts import render
from rest_framework.views import APIView
import random
from django.core.mail import send_mail
from .models import User
from rest_framework.response import Response
from django.template.loader import get_template
from rest_framework.validators import ValidationError

class EmailVarification(APIView):
    gen_otp = random.randint(100000,999999)
    def get(self,request):
        user = User.objects.get(user_id=request.user.user_id)
        email = user.email
        subject, from_email, to = 'Varification',None,email
        context = {
            "username":user.username,
            "otp":self.gen_otp
        }

        subject = "verify your email"
        sent = send_mail(
            subject=subject,
            message = "hello",
            html_message=get_template('email.html').render(context),
            from_email = None,
            recipient_list = [email])
        if sent:
            return Response({"msg":"email has been sent"})
        raise ConnectionError()
        

    def post(self,request):
        user = User.objects.filter(user_id=request.user.user_id)
        data = request.data
        otp = data["otp"]
        if str(otp) == str(self.gen_otp):
            user.update(is_verified=True)
            return Response({"msg":"email is verified"})
        return ValidationError(detail="you are entering wrong otp",code=400)



