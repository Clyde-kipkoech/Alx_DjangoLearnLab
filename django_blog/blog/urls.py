from django.urls import path, include

urlpatterns = [
    # exposes /register/, /login/, /logout/, /profile/
    path('', include('accounts.urls')),
    # add additional blog URLs below as needed
]
