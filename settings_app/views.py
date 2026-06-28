from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from consultation.models import Notification

from .models import SiteSetting
from .forms import SiteSettingForm


@login_required
def settings(request):

    notification_count = Notification.objects.filter(
        is_read=False
    ).count()

    setting, created = SiteSetting.objects.get_or_create(
        id=1
    )

    form = SiteSettingForm(
        request.POST or None,
        request.FILES or None,
        instance=setting
    )

    if form.is_valid():

        form.save()

        return redirect("settings")

    return render(

        request,

        "dashboard/settings/settings.html",

        {

            "form": form,

            "notification_count": notification_count,

        }

    )