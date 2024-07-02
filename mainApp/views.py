from random import randint
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from django.utils import timezone
import os

from Earning import settings


from .models import *

def home(request):
    return render(request,"index.html")

@login_required(login_url="/login/")
def me(request):
    buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))

    now = datetime.datetime.now()
    time = now.time()
    time = str(time)
    time = time.split(":")
    hour = time[0]
    min = time[1]
    if(int(hour)==12 & int(min) == 00):
        buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
        buyer.dailyincome = 27
        buyer.totalamount=buyer.totalamount+27
        buyer.save()
    print(hour)
    print(min)

    return render(request,"me.html",{'User':buyer})

@login_required(login_url="/login/")
def withdrawn(request):
    buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
    return render(request,"withdrawn.html",{'User':buyer})

@login_required(login_url="/login/")
def invite(request):
    buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
    return render(request,"invite.html",{'User':buyer})

@login_required(login_url="/login/")
def idetails(request):
    buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
    buyer = Reff.objects.filter(invite=buyer)
    return render(request,"idetails.html",{'Invitation':buyer})

@login_required(login_url="/login/")
def rdetails(request):
    buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
    buyer = Recharge.objects.filter(buyer=buyer)
    return render(request,"rechargedetails.html",{'Recharge':buyer})

@login_required(login_url="/login/")
def bdetails(request):
    buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
    buy = Buy.objects.filter(buyer=buyer)
    return render(request,"buydetails.html",{'Product':buy})

@login_required(login_url="/login/")
def income(request,num):
    buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
    buy = Buy.objects.get(id=num)
    if buy.can_click():
        if request.method == "POST":
            buyer.balance+=buy.product.income
            buyer.dailyincome+=buy.product.income
            buy.wallet += buy.product.income
            buy.last_clicked = timezone.now()
            buy.save()
            buyer.save()
            messages.success(request, 'Income added to your wallet!')
    else:
        messages.error(request, 'You can only click the button once every 24 hours!')
    return render(request,"generateincome.html",{'Product':buy})

@login_required(login_url="/login/")
def wdetails(request):
    buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
    buyer = Withdrawn.objects.filter(buyer=buyer)
    return render(request,"wdetails.html",{'Recharge':buyer})

@login_required(login_url="/login/")
def updatewithdrawn(request):
    bank = Bank.objects.all()
    if request.method == "POST":
        u = Buyer.objects.get(phone=User.objects.get(username=request.user))
        u.bank = request.POST.get("bank")
        u.name = request.POST.get("name")
        u.account = request.POST.get("account")
        u.ifsc = request.POST.get("ifsc")
        u.password = request.POST.get("password")
        u.save()
        messages.success(request, "Sucessfully Updated !")
        return HttpResponseRedirect("/withdrawn/")
    return render(request,"withdrawnupdate.html",{'Bank':bank})

@login_required(login_url="/login/")
def withd(request):
    buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
    if request.method == "POST":
        u = Withdrawn()
        u.bank = buyer.bank
        u.name = buyer.name
        u.account = buyer.account
        u.ifsc = buyer.ifsc
        u.buyer=buyer
        amount = request.POST.get("amount")
        password = request.POST.get("password")
        try:
            if(int(amount)<=buyer.totalamount):
                if(password == buyer.password):
                    if(int(amount)>=110):
                        u.amount=amount
                        buyer.totalamount=(buyer.totalamount)-int(amount)
                        buyer.save()
                        u.save()
                        messages.success(request, "Sucessfully Withdrawn !")
                    else:
                        messages.success(request, "Amount less than 110 !")
                else:
                    messages.error(request, "Password Doesn't Match !")
            else:
                messages.error(request, "Invalid Amount !")
        except:
            messages.error(request, "Invalid Amount or Password !")
    return render(request,"with.html",{'User':buyer})

@login_required(login_url="/login/")
def recharge(request):
    if request.method == "POST":
        u=Recharge()
        buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
        u.buyer= buyer
        amount = request.POST.get("amount")
        u.amount = amount
        if(int(amount)>100):
            buyer.rech+=int(amount)
            buyer.save()
            u.save()
            messages.success(request, "Recharge Success !")
            return HttpResponseRedirect("/me/")
        else:
            messages.success(request, "Amount less than 100 !")
    return render(request,"recharge.html")

def login(request):
    if request.method == "POST":
            try:
                phone = request.POST.get("phone")
                password = request.POST.get("password")
                user = auth.authenticate(username=phone, password=password)
                if user is not None:
                    auth.login(request, user)
                    if user.is_superuser:
                        return HttpResponseRedirect("/admin/")
                    else:
                        return HttpResponseRedirect("/")
                else:
                    messages.error(request, "Invalid Phone Number or Password")
            except:
                return HttpResponseRedirect("/login/")
    return render(request,"login.html")

def signup(request):
    if request.method == "POST":
        u = Buyer()
        phone = request.POST.get("phone")
        u.phone=phone
        u.email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        referral = request.POST.get("referral")
        ref=0
        def ref():
            ref = randint(100000,999999)
            u.referral = ref
        if password == cpassword:
            try:  
                us = Buyer.objects.get(referral=referral)
                r = Reff()
                r.buyer=phone
                r.invite=us
                r.save()
                try:
                    user = User.objects.create_user(
                            username=u.phone, password=password, email=u.email
                    )
                    user.save()
                    try:
                        ref()
                        u.save()
                    except:
                        ref()
                        u.save()
                    messages.success(request, "Account Created Sucessfully....")
                    return HttpResponseRedirect("/login/")        
                except:
                    messages.error(request, "Phone number already Exists...")
                    return render(request, "login.html")
            except:
                messages.error(request, "Invalid Invitation Code ...")
        else:
            messages.error(request, "Password and Confirm Password does not matched!!!!"
                )
    return render(request, "signup.html")

@login_required(login_url="/login/")
def shop(request):
    product =Product.objects.all()
    products = product[::-1]
    return render(request,"shop.html",{'Product':products})

@login_required(login_url="/login/")
def singleproduct(request, num):
    p = Product.objects.get(id=num)
    if request.method == "POST":
        buyer = Buyer.objects.get(phone=User.objects.get(username=request.user))
        if(buyer.rech>p.baseprice):
            buyer.rech=buyer.rech-p.baseprice
            buyer.product=buyer.product+p.baseprice
            buyer.save()
            buy = Buy()
            buy.buyer=buyer
            buy.product=p
            buy.save()
            return HttpResponseRedirect("/me/")   
        else:
            messages.error(request, "Recharge Now !")
    return render(request, "singleProduct.html",{'Product':p})

@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

def forgetusername(request):
    if(request.method=='POST'):
        try:
            phone = request.POST.get("phone")
            user = User.objects.get(username=phone)
            print(user)
            if(user is not None):
                try:
                    user = Buyer.objects.get(phone=User.objects.get(username=phone))
                except:
                    pass
                num = randint(100000,999999)
                request.session['otp']=num
                request.session['user']=phone
                print(num)
                return HttpResponseRedirect("/forgetotp/")
            else:
                messages.error(request,'Username not Found')
        except:
            messages.error(request,'Username not Found')
    return render(request,'forgetusername.html')

def forgetotp(request):
    if(request.method=='POST'):
        otp = int(request.POST.get("otp"))
        sessionotp = request.session.get('otp',None)
        if(otp == sessionotp):                  
            return HttpResponseRedirect('/forgetpassword/')
        else:
            messages.error(request,'Invalid OTP') 
    return render(request,'forgetotp.html')

def forgetpassword(request):
    if(request.method=='POST'):
        password = (request.POST.get("password"))
        cpassword = (request.POST.get("cpassword"))
        if(password == cpassword): 
            user = User.objects.get(username = request.session.get('user'))
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/login/')
        else:
            messages.error(request,"Password and Confirm Doesn't Match")
    return render(request,'forgetpassword.html')