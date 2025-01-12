from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from account.forms import CustomUserRegistrationForm, CustomUserLoginForm, UserUpdateForm, ProfileUpdateForm
from account.models import VIPPackage, CustomUser, News, VIPPackagePurchase
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone


def register(request):
    referrer = None
    ref_code = request.GET.get('ref')

    if ref_code:
        referrer = CustomUser.objects.filter(referral_link=ref_code).first()
        if not referrer:
            messages.error(request, "Berilgan referal kod noto‘g‘ri.")
            return redirect('register')

    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            if referrer:
                referrer.team.add(user)
                referrer.save()

            login(request, user)
            messages.success(request, "Ro‘yxatdan muvaffaqiyatli o‘tdingiz!")
            return redirect('home')
        else:
            messages.error(request, "Iltimos, xatolarni to‘g‘rilang.")
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'account/register.html', {'form': form, 'referrer': referrer})


def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def home(request):
    return render(request, 'account/home.html')


@login_required
def vip_package(request):
    packages = VIPPackage.objects.all()
    return render(request, 'account/vip_package.html', {'packages': packages})


@login_required
def my_account(request):
    user = request.user

    team_members = user.team.all()

    now = timezone.now()
    active_vip_packages = []
    for package in user.vip_packages.all():
        purchase_entry = VIPPackagePurchase.objects.filter(user=user, package=package).first()
        if purchase_entry:
            expiry_date = purchase_entry.start_date + timedelta(days=package.duration)
            if expiry_date >= now:
                active_vip_packages.append(package)

    expired_packages = user.vip_packages.exclude(id__in=[p.id for p in active_vip_packages])
    expired_packages.delete()

    daily_income = user.calculate_daily_income()

    if request.method == 'POST' and 'package_id' in request.POST:
        package_id = request.POST.get('package_id')
        if package_id:
            package = VIPPackage.objects.get(id=package_id)
            referrer = user.team.first()

            vip_package_purchase = VIPPackagePurchase.objects.create(
                user=user,
                package=package,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=package.duration)
            )

            if referrer:
                referrer.my_money += vip_package_purchase.package.daily_income * 0.03
                referrer.save()

            user.vip_packages.add(package)
            user.save()

            messages.success(request, f"You have successfully purchased {package.name}!")
            return redirect('account:my_account')

    if request.method == 'POST' and 'update_profile' in request.POST:
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('account:my_account')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'team_members': team_members,
        'active_vip_packages': active_vip_packages,
        'my_money': user.my_money,
        'daily_income': daily_income,
        'full_name': user.full_name,
        'image': user.image,
        'bio': user.bio,
        'referral_link': user.referral_link,
        'generate_id': user.generate_id,
    }
    return render(request, 'account/my_account.html', context)


@login_required
def news_(request):
    news_list = News.objects.all()
    user = request.user

    if request.method == 'POST':
        news_id = request.POST.get('news_id')
        news_item = News.objects.get(id=news_id)

        if news_item.likes.filter(id=request.user.id).exists():
            news_item.likes.remove(request.user)
            request.user.my_money -= user.daily_income
        else:
            news_item.likes.add(request.user)
            request.user.my_money += user.daily_income

        request.user.calculate_daily_income()

        request.user.save()
        return redirect('news')

    return render(request, 'account/news.html', {'news': news_list})
