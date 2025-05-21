from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# FBV "login_view"
def login_view(request):
    # Initializes error_message as None
    error_message = None

    # Form object of class AuthenticationForm
    form = AuthenticationForm()

    # Generates POST request when user clicks "Login"
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        # Checks form validity
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Validates user
            user = authenticate(username=username, password=password)

            # Logs user in if validated
            if user is not None:
                login(request, user)
                return redirect('recipes:list')
            else:
                error_message = 'Something went wrong. Try again later.'

    # Prepares data to send from view to template
    context = {
        'form': form,
        'error_message': error_message
    }

    # Loads login page using "context" information
    return render(request, 'auth/login.html', context)    

# FBV "logout_view"
def logout_view(request):
  logout(request)
  return render(request, 'auth/success.html')