from django.contrib import admin
from .models import *
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','baseprice','term','purchaselimit','income','earning','totalyield','description','desc1','desc2','desc3','desc4','desc5','stock','pic1','pic2','pic3']

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['id','phone','email','name','account','referral','dailyincome','product','rech','balance','ifsc','bank','password']

@admin.register(Withdrawn)
class WithdrawnAdmin(admin.ModelAdmin):
    list_display = ['id','buyer','name','account','ifsc','bank','amount','date','status']

@admin.register(Recharge)
class RechargeAdmin(admin.ModelAdmin):
    list_display = ['id','buyer','amount','date']

@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ['id','buyer','product','date','wallet','last_clicked']

@admin.register(Reff)
class ReffAdmin(admin.ModelAdmin):
    list_display = ['id','buyer','invite','date']