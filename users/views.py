from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from users import forms, models

from order.models import ShopCart
from order.views import total_price
from main.views import total_price_items


def register(request):

    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in.')
            return redirect('users:login')
    else:
        form = forms.UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required(login_url='/users/login')
def profile(request):

    context = {
        'profiles': models.Profile.objects.filter(user_id=request.user.id),
    }
    context.update(total_price_items(request.user.id))
    return render(request, 'users/profile.html', context)


@login_required(login_url='/users/login')
def profile_update(request):
    
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        user_form = forms.UserUpdeteForm(request.POST, instance=request.user)
        profile_form = forms.ProfileUpdeteForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return HttpResponseRedirect('/users/profile')
        else:
            messages.warning(
                request, 'Your Profile was not successfully updated!')
            return HttpResponseRedirect('/users/profile')

    user_form = forms.UserUpdeteForm(instance=request.user)
    profile_form = forms.ProfileUpdeteForm(instance=profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    context.update(total_price_items(request.user.id))
    return render(request, "users/update_profile.html", context)



