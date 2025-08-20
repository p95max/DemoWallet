from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def notifications_list(request):
    notifications = request.user.notifications.all()
    if request.method == "POST" and "mark_all_read" in request.POST:
        notifications.filter(is_read=False).update(is_read=True)
        return redirect('notifications:notifications_list')

    context = {
        'notifications': notifications,
    }

    return render(request, "notification/list.html", context=context)