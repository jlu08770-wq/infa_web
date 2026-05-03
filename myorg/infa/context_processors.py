from .models import InfaModelProfile, InfaUser


def infa_auth(request):
    user = None
    profile = None
    user_id = request.session.get('infa_user_id')

    if user_id:
        user = InfaUser.objects.filter(pk=user_id).first()
        if user and user.role == 'model':
            profile = InfaModelProfile.objects.select_related('user').filter(user=user).first()

    return {
        'current_user': user,
        'current_profile': profile,
    }
