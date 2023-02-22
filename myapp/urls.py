from django.urls import path
from .views import *


urlpatterns=[
    path('first1/',first),
    path('ind/',ind),
    path('shopregister/',shopreg),
    path('userregister/',userreg),
    path('shoplogin/',shoplog),
    path('userlogin/',userlog),
    path('profile/',profpage),
    path('productupload/',productupload),
    path('productdisplay/',productdisplay),
    path('delete/<int:id>',productdelete),
    path('edit/<int:id>',productedit),
    path('verify/<auth_token>',verify),
    path('userproddisp/',userproduct),
    path('userprof/',userprof),
    path('addcart/<int:id>',addcart),
    path('wishlistuser/<int:id>',wishlistuser),
    path('cartdisplay/',cartdisplay),
    path('wishlistdisplay/',wishlistdisplay),
    path('removecart/<int:id>',removecart),
    path('wishlistremove/<int:id>',wishlistremove),
    path('cartbuy/<int:id>',cartbuy),
    path('order/<int:id>',order),
    path('customerdetails/',details),
    path('summary/',summary),
    path('viewallproducts/',viewallproducts),
    path('shop_notification/',shop_notification),
    path('user_notification/',user_notification)


]