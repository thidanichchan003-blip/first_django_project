def user_roles(request):

    is_consultant = False

    if request.user.is_authenticated:
        is_consultant = request.user.groups.filter(
            name='Consultant'
        ).exists()

    return {
        'is_consultant': is_consultant
    }