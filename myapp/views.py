from django.contrib.auth import authenticate
from django.core.mail import send_mail
from myproject.settings import EMAIL_HOST_USER
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
import datetime
from datetime import timedelta

# Create your views here.

def first(request):
    return HttpResponse("hello developers")

def ind(request):
    return render(request,'index.html')
def shopreg(request):
    if request.method=='POST':
        a=shopregform(request.POST)
        if a.is_valid():
            sn=a.cleaned_data["shop_name"]
            lc=a.cleaned_data["location"]
            idn=a.cleaned_data["idm"]
            em=a.cleaned_data["mail"]
            hp=a.cleaned_data["ph"]
            ps=a.cleaned_data["password"]
            cp=a.cleaned_data["cfmpass"]
            if ps==cp:
                b=shopregmodel(shop_name=sn,location=lc,idm=idn,mail=em,ph=hp,password=ps)
                b.save()
                return redirect(shoplog)
            else:
                return HttpResponse("password dosn't match")
        else:
            return HttpResponse("registration failed")
    return render(request,'shop_register.html')
def shoplog(request):
    if request.method=='POST':
        a=shoplogform(request.POST)
        if a.is_valid():
            sn=a.cleaned_data["shop_name"]
            ps=a.cleaned_data["password"]
            request.session['shopname']=sn
            b=shopregmodel.objects.all()
            for i in b:
                if sn==i.shop_name and ps==i.password:
                    request.session['id']=i.id
                    return redirect(profpage)
            else:
                return HttpResponse("login failed")
    return render(request,'shop_login.html')

def profpage(request):
    shopname=request.session['shopname']

    return render(request,'profile_page.html',{'shopname':shopname})

def userreg(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')

        #checking whether the username exists
        if User.objects.filter(username=username).first(): #username
            ## it will get first object from filter query.
           messages.success(request,'username already taken')

           return redirect(userreg)
        if User.objects.filter(email=email).first():
           messages.success(request,'email already exist')
           return redirect(userreg)
        user_obj=User(username=username,email=email,first_name=firstname,last_name=lastname)
        user_obj.set_password(password)
        user_obj.save()

        #import uuid
        #uuid module
        auth_token=str(uuid.uuid4())
        # new model created
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        #user defined function
        send_mail_regis(email,auth_token) #mail sending function
        return render(request,'success.html')
    return render(request,'user_register.html')

def send_mail_regis(email,auth_token):
    subject="your account has been verified"
    message=f'click the link to verified your account http://127.0.0.1:8000/myapp/verify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    # inbuild function
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj: #true
        if profile_obj.is_verified:
            messages.success(request,'your account is alrerady verified')
            return redirect(userlog)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(userlog)
    else:
        messages.success(request,"user not found")
        return redirect(userlog)

def userlog(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        request.session['username']=username
        user_obj =User.objects.filter(username=username).first()
        #user_obj=favaz

        if user_obj is None:#if user doesn't exist
            messages.success(request,'user not found')
            return redirect(userlog)
        profile_obj = profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified: #if not profile is_verified

            messages.success(request,'profile not verified check your mail')
            return redirect(userlog)

        user = authenticate(username=username, password=password)
        #user=valid
        #if the given credentials are valid, return a user object.
        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(userlog)
        request.session['uid'] = user_obj.id
        return redirect(userprof)
    return render(request,'user_login.html')



def productupload(request):
    if request.method=='POST':
        a=productform(request.POST,request.FILES)
        id=request.session['id']
        if a.is_valid():
            pn=a.cleaned_data['productname']
            p=a.cleaned_data['price']
            d=a.cleaned_data['discription']
            im=a.cleaned_data['image']
            b=productmodel(shopid=id,productname=pn,price=p,discription=d,image=im)
            b.save()
            return redirect(productdisplay)
        else:
            return HttpResponse("upload failed")
    return render(request, 'file_upload.html')

def productdisplay(request):
    shpid=request.session['id']
    a = productmodel.objects.all()
    imagepd = []
    name = []
    pr=[]
    des=[]
    id=[]
    shopid=[]
    for i in a:
        sid=i.shopid
        shopid.append(sid)
        id1=i.id
        id.append(id1)
        im = i.image
        imagepd.append(str(im).split('/')[-1])
        nm = i.productname
        name.append(nm)
        prs = i.price
        pr.append(prs)
        dcrn = i.discription
        des.append(dcrn)
    mylist = zip(imagepd, name,pr,des,id,shopid)
    return render(request, 'productdisp.html', {'mylist': mylist,'shpid':shpid})

def productdelete(request,id):
    a=productmodel.objects.get(id=id)
    a.delete()
    return redirect(productdisplay)

def productedit(request,id):
    a=productmodel.objects.get(id=id)
    im=str(a.image).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES): #to check the new file
            if len(a.image)>0: # to check old file
                os.remove(a.image.path)
            a.image=request.FILES['image']
        a.productname=request.POST.get('prodname')
        a.price=request.POST.get('price')
        a.discription=request.POST.get('des')
        a.save()
        return redirect(productdisplay)
    return render(request,'editproduct.html',{'a':a,'im':im})

def userproduct(request):
    a = productmodel.objects.all()
    imagepd = []
    name = []
    pr = []
    des = []
    id = []
    for i in a:
        id1 = i.id
        id.append(id1)
        im = i.image
        imagepd.append(str(im).split('/')[-1])
        nm = i.productname
        name.append(nm)
        prs = i.price
        pr.append(prs)
        dcrn = i.discription
        des.append(dcrn)
    mylist = zip(imagepd, name, pr, des, id)
    return render(request, 'userproduct disp.html', {'mylist': mylist})


def userprof(request):
    a=request.session['username']
    return render(request,'user profile.html',{'a':a})
def addcart(request,id):
    u_id = request.session['uid']
    a=productmodel.objects.get(id=id)
    if cart.objects.filter(productname=a.productname):
        messages.success(request, 'product is already in cart')
        return redirect(userprof)
    else:
        b = cart(user_id=u_id, productname=a.productname, price=a.price, discription=a.discription, image=a.image)
        b.save()
    return redirect(userprof)


   # return render(request,'usercart.html')




def wishlistuser(request,id):
    u_id =request.session['uid']
    a = productmodel.objects.get(id=id)
    if wishlist.objects.filter(productname=a.productname):
        messages.success(request, 'product is already in wishlist')
        return redirect(userprof)
    else:
        b = wishlist(user_id=u_id, productname=a.productname, price=a.price, discription=a.discription, image=a.image)
        b.save()
    return redirect(userprof)



def wishlistdisplay(request):
    u_id= request.session['uid']
    a=wishlist.objects.all()
    imagepd = []
    name = []
    pr = []
    des = []
    id = []
    user_id = []
    for i in a:
        id1 = i.id
        id.append(id1)
        im = i.image

        imagepd.append(str(im).split('/')[-1])
        nm = i.productname
        name.append(nm)
        prs = i.price
        pr.append(prs)
        dcrn = i.discription
        des.append(dcrn)
        us_id = i.user_id
        user_id.append(us_id)
    mylist = zip(imagepd, name, pr, des,id, user_id)
    return render(request, 'wishlist.html', {'mylist': mylist, 'u_id': u_id})

def cartdisplay(request):
    u_id = request.session['uid']
    a = cart.objects.all()
    imagepd = []
    name = []
    pr = []
    des = []
    id = []
    user_id = []
    for i in a:
        id1 = i.id
        id.append(id1)
        im = i.image
        imagepd.append(str(im).split('/')[-1])
        nm = i.productname
        name.append(nm)
        prs = i.price
        pr.append(prs)
        dcrn = i.discription
        des.append(dcrn)
        us_id = i.user_id
        user_id.append(us_id)
    mylist = zip(imagepd, name, pr, des,id,user_id )
    return render(request, 'cart.html', {'mylist': mylist, 'u_id': u_id})

# return render(request,'wishlist.html')
def removecart(request,id):
    a=cart.objects.get(id=id)
    a.delete()
    return redirect(cartdisplay)

def wishlistremove(request,id):
    a=wishlist.objects.get(id=id)
    a.delete()
    return redirect(wishlistdisplay)

def cartbuy(request,id):
    a=cart.objects.get(id=id)
    img=str(a.image).split('/')[-1]
    if request.method=='POST':
        pn=request.POST.get('productname')
        pp=request.POST.get('price')
        pq=request.POST.get('quantity')
        b=buy(productname=pn,price=pp,quantity=pq)
        b.save()
        total=int(pp)*int(pq)
        return render(request,'finalbill.html',{'b':b,'total':total})

    return render(request,'buyproduct.html',{'a':a,'img':img})

def order(request,id):
    return render(request,'finalbill.html')

def details(request):
    if request.method=='POST':
        card_holder_name= request.POST.get('card_holder_name')
        card_number= request.POST.get('card_number')
        date= request.POST.get('date')
        security_code= request.POST.get('security_code')
        user_obj=customerdetails1(card_holder_name=card_holder_name,card_number=card_number,date=date,security_code=security_code)
        user_obj.save()
        today = datetime.date.today()
        today +=timedelta(days=10)
        return render(request,'order_summary.html',{'today': today})

    return render(request,'customer_details.html')

def summary(request):
    return render(request,'order_summary.html')

def viewallproducts(request):
    return render(request,'othershop.html')

def shop_notification(request):
    a=shopnotification.objects.all()
    m_content = []
    m_date = []
    for i in a:
        mc = i.content
        m_content.append(mc)
        md = i.date
        m_date.append(md)
    mylist = zip(m_content,m_date)
    return render(request,'shpnotification.html',{'mylist': mylist})

def user_notification(request):
    a = usernotification.objects.all()
    m_content = []
    m_date = []
    for i in a:
        mc = i.content
        m_content.append(mc)
        md = i.date
        m_date.append(md)
    mylist = zip(m_content, m_date)
    return render(request, 'usrnotification.html', {'mylist': mylist})





