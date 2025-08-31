# file: main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def homepage_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_hub")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard_hub")
    else:
        form = AuthenticationForm()

    return render(request, "main/homepage.html", {"form": form})


@login_required
def dashboard_hub_view(request):
    user = request.user
    if hasattr(user, "nhanvien"):
        nhanvien = user.nhanvien
        if nhanvien.phong_ban:
            phong_ban_name = nhanvien.phong_ban.ten_phong_ban.lower()
            if "kinh doanh" in phong_ban_name:
                return redirect("clients:pipeline")
            if "nghiệp vụ" in phong_ban_name:
                if (
                    nhanvien.chuc_danh
                    and "quản lý" not in nhanvien.chuc_danh.ten_chuc_danh.lower()
                ):
                    return redirect(
                        "operations:mobile_dashboard"
                    )  # Giả định có URL này
                return redirect("operations:xep-lich")

    # Dành cho Ban Giám đốc, các vai trò khác và superuser
    return redirect("dashboard:main")
