
def user_profile_picture(request):
    if request.user.is_authenticated:
        return {'profile_picture': request.user.profile_picture}
    return {}