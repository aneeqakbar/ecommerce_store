from shop.models import Product
from django.http.response import Http404
from user.models import Address, Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View,ListView,DetailView
from django.contrib import messages
from .forms import AddAddressForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

class SignUpView(View):
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('core:HomeView'))
        form = CustomUserCreationForm()
        context={'form':form}
        return render(self.request,'auth/signup.html',context)

    def post(self,*args, **kwargs):
        form = CustomUserCreationForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            user = form.save()
            user.profile.profile_pic = self.request.FILES['profile_pic']
            user.profile.mobile_number = self.request.POST['phone']
            user.profile.save()
            messages.success(self.request,'Account Created Successfully')
            login(self.request,user)
            return HttpResponseRedirect(reverse('core:HomeView'))
        else:
            context = {'form':form}
            return render(self.request,'auth/signup.html',context)

class LoginView(View):
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('core:HomeView'))
        form = AuthenticationForm()
        context={'form':form}
        return render(self.request,'auth/login.html',context)

    def post(self,*args, **kwargs):
        next_page = self.request.POST['next'] #get the next page (the user coming from) in case if one exists

        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(self.request, username =username, password = password)
        if user is not None:
            user_logged_in.send(sender=user.__class__,request=self.request,user=user)
            login(self.request,user)
            if next_page:
                return HttpResponseRedirect(next_page)
            return HttpResponseRedirect(reverse('core:HomeView'))
        else:
            form = AuthenticationForm()
            context = {'form':form}
            messages.error(self.request,'Invalid Credentials')
            return render(self.request,'auth/login.html',context)

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def post(self,*args, **kwargs):
        logout(self.request)
        return redirect('core:HomeView') # because the logout form is in Home page thats why i cant use HttpResponseRedirect(reverse('core:HomeView')) here

class AddAddressView(View):
    def get(self,*args, **kwargs):
        form = AddAddressForm()
        context = {'form':form}
        return render(self.request,'auth/add_address.html',context)
    def post(self,*args, **kwargs):
        form = AddAddressForm(self.request.POST)
        context = {'form':form}
        if form.is_valid():
            profile = Profile.objects.filter(user = self.request.user).first()
            if profile.address is not None:
                address = form.save()
                profile.address.delete()
                profile.address = address
                messages.success(self.request,'Address updated Successfully')
            else:
                address = form.save() 
                profile.address = address
                profile.save()
                messages.success(self.request,'Address Added Successfully')
            return HttpResponseRedirect(reverse('core:HomeView'))
        return HttpResponseRedirect(reverse('user:AddAddressView',context))

class DetailUserView(View):
    def get(self,*args, **kwargs):
        current_user = get_object_or_404(User,pk = kwargs['pk'])
        products = current_user.products.all()
        all_products = products.order_by('-created_on')

        paginator = Paginator(all_products, per_page=8)
        page = self.request.GET.get('page',1)
        products = paginator.get_page(page)
        if self.request.META.get('CONTENT_TYPE') == 'application/json':
            try:
                products = paginator.page(page)
            except EmptyPage:
                raise Http404
            except PageNotAnInteger:
                products = paginator.page(1)
            return render(self.request, 'generate_products.html', {'products' : products})
        context = {'user_products':products.object_list,'current_user':current_user}
        return render(self.request,'auth/user_details.html',context)





# ______________________________________________________________________ #
def logged_IN(sender, user, request, **kwargs):
    print('LOGGED IN',user.username)

user_logged_in.connect(logged_IN)