from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def debug_user_type(request):
    user_type = request.user.user_type
    user_type_repr = repr(user_type)
    user_type_type = type(user_type).__name__
    
    response_text = (
        f"User: {request.user.username}<br>"
        f"user_type: {user_type}<br>"
        f"user_type repr: {user_type_repr}<br>"
        f"user_type type: {user_type_type}<br>"
        f"Comparison with 'doctor': {user_type == 'doctor'}<br>"
        f"Comparison repr: {repr(user_type) == repr('doctor')}<br>"
        f"ASCII Values user_type: {[ord(c) for c in user_type]}<br>"
        f"ASCII Values 'doctor': {[ord(c) for c in 'doctor']}<br>"
    )
    
    return HttpResponse(response_text)
