from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import (
    redirect,
    render,
)


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


def home(request):
    return render(request, "accounts/home.html")


@login_required
def profile(request):
    return render(request, "accounts/profile.html", {"user": request.user})
