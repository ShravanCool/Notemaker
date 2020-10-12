from .forms import SearchBarform

def SearchBar(request):
    """
    Produces a context variable for the searchbar that's available across
    all pages.
    """
    return {'searchbar': SearchBarForm()}

def SetCurrentCourses(request):
    """
    Produces a context variable for all user's current courses that's 
    available across all pages.
    """
    user = request.user

    try:
        current_term = user.terms.all().filter(user=user, current=True)[0]
        current_courses = current_term.courses.all()
    except (AttributeError, IndexError):
        current_courses = None

    return {'current_courses': current_courses}
