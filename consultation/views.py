from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Consultation, Message, Notification
from .forms import ConsultationForm


@login_required
def consultation_create(request):

    consultation = Consultation.objects.filter(
        user=request.user,
        status='Open'
    ).first()

    if not consultation:
        consultation = Consultation.objects.create(
            user=request.user
        )

    return redirect(
        'consultation_chat',
        consultation_id=consultation.id
    )


@login_required
def consultation_list(request):

    if (
        request.user.is_staff
        or request.user.groups.filter(name='Consultant').exists()
    ):

        consultations = Consultation.objects.all().order_by('-id')

        return render(
            request,
            'consultation/list.html',
            {
                'consultations': consultations
            }
        )

    consultation = Consultation.objects.filter(
        user=request.user
    ).order_by('-id').first()

    if consultation:
        return redirect(
            'consultation_chat',
            consultation_id=consultation.id
        )

    return redirect('consultation_create')


@login_required
def consultation_chat(request, consultation_id):

    consultation = get_object_or_404(
        Consultation,
        id=consultation_id
    )

    if (
        not request.user.is_staff
        and not request.user.groups.filter(name='Consultant').exists()
        and consultation.user != request.user
    ):
        return redirect('consultation_list')

    if request.method == 'POST':

        text = request.POST.get('message')

        if text:

            Message.objects.create(
                consultation=consultation,
                sender=request.user,
                message=text
            )

            # Create notification for all admin users
            admins = User.objects.filter(is_staff=True)

            for admin in admins:
                Notification.objects.create(
                    title="New Consultation",
                    message=f"{request.user.username} sent a new consultation.",
                    notification_type="consultation",
                    link=f"/consultation/chat/{consultation.id}/"

                )

            return redirect(
                'consultation_chat',
                consultation_id=consultation.id
            )

    messages = consultation.messages.all().order_by(
        'created_at'
    )

    return render(
        request,
        'consultation/chat.html',
        {
            'consultation': consultation,
            'messages': messages
        }
    )