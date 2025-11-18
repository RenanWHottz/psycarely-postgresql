from django.shortcuts import redirect


def root_redirect(request):
    """Redireciona a raiz do site para a página de login."""
    return redirect('login')
