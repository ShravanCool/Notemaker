from django.shortcuts import render, resolve_url, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.wdit import (CreateView, UpdateView, DeleteView,
                                       FormView,)
from django.views.generic.list import ListView
from rest_framework import permissions, viewsets
from .forms import (TermForm, CourseForm, ClassNoteForm, CourseOfTermForm,
                    UpdateNoteForm, SearchBarForm, CurrentTermForm)
from .models import Term, Course, ClassNote
from .serializers import TermSerializer, CourseSerializer, ClassNoteSerializer

def SearchBar(request):
    """
    Redirects active-user to a ClassNote object's DetailView given the data that
    they provide to the searchbar. ClassNote objects are retrieved by
    title. If multiple matches are made, user is provided a list of all similar
    hits; refer to NotesListSearchQuery class. If no matches can be made user is
    shown all ClassNote objects.
    """
    redirect_url = reverse_lazy('Notes:notes_list')

    if request.method == 'GET':

        user = request.user
        notes = user.notes.all()

        if notes:
            title = ''.join(request.GET['title'].lower.split(' '))

            matches = []
            for note in notes:
                if title in note.join_title():
                    course = note.course
                    term = note.term
                    args = [term.term_slug, course.course_slug, note.note_slug]
                    redirect_url = reverse_lazy("Notes:one_note", args=args)
                    matches.append(note.note_slug)

            if len(matches) > 1:
                args = ['+'.join(matches)]
                redirect_url = reverse_lazy('Notes:notes_search',args=args)

    return HttpResponseRedirect(redirect_url)


class TermViewSet(viewsets.ModelViewSet):
    """
    Displays the JSON data of all Term objects associated with the active-user.
    """
    serializer_class = TermSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Retrieves all term objects associated with the active_user; otherwise
        returns an empty queryset for other users.
        """
        active_user = self.request.user
        if active_user.is_authenticated:
            queryset = Term.objects.filter(user=active_user)
        else:
            queryset = Term.objects.none()
        return queryset


class CourseViewSet(viewsets.ModelViewSet):
    """
    Displays the JSON data of all Course objects associated with the active-user.
    """
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Retrieves all Course objects associated with the active_user; otherwise
        returns an empty queryset for other users.
        """
        active_user = self.request.user
        if active_user.is_authenticated:
            queryset = Course.objects.filter(user=active_user)
        else:
            queryset = Course.objects.none()
        return queryset


class ClassNoteViewSet(viewsets.ModelViewSet):
    """
    Displays the JSON data of all ClassNote objects associated with the active-user.
    """
    serializer_class = ClassNoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Retrieves all ClassNote objects associated with the active_user; otherwise
        returns an empty queryset for other users.
        """
        active_user = self.request.user
        if active_user.is_authenticated:
            queryset = ClassNote.objects.filter(user=active_user)
        else:
            queryset = ClassNote.objects.none()
        return queryset


class CreateTermView(CreateView,ListView):
    """
    Displays form for Term creation and lists all term objects related to
    active-user.
    """
    template_name = 'term.html'
    form_class = TermForm
    context_object_name = 'terms'
    success_url = reverse_lazy('Notes:term')

    def form_valid(self, form):
        """
        Creates a new Term object goven the valid form
        """
        term_form = TermForm(self.request.POST)
        term = term_form.save(commit = False)
        term.user = self.request.user
        term.term_slug = slugify(term.session)
        term.save()
        return HttpResponseRedirect(self.success_url)

    def queryset(self):
        """
        Retrieves queryset of all Term objects related to the active user.
        """
        active_user = self.request.user
        queryset = active_user.terms.all()
        return queryset


class UpdateOptionsTerm(FormView, ListView):
    """
    View for choosing current term, deleting a term, or access the term object
    update page.
    """
    template_name = 'term_edit_delete.html'
    context_object_name = 'terms'
    form_class = CurrentTermForm
    success_url = reverse_lazy('Notes:term')

    def get_queryset(self):
        """
        Retrieves Term objects related to active user
        """
        user = self.request.user
        queryset = user.terms.all()
        return queryset

    def get_context_data(self,**kwargs):
        """
        Provides extra context variables in addition to giving the form a more 
        sensible context variable name
        """
        context = super().get_context_data(**kwargs)
        context['editing'] = True
        context['current_term_form'] = context.get('form')
        return context

    def get_terms(self):
        """
        Custom method that retrieves a queryset containing all of the 
        active-user's Term objects and produces a list of two-item tuples
        """
        user = self.request.user
        terms = user.terms.all()
        choices = [('','Select current term')]
        choices += [(i,j) for i,j in zip(terms,terms)]
        return choices

    def get_form_kwargs(self):
        """
        Passes the list of two-item tuples returned via the get-terms method to 
        the form to be used as selectable choices.
        """
        kwargs = super().get_form_kwargs()
        kwargs['term_choices'] = self.get_terms()
        return kwargs

    def set_current_term(self,current_term):
        """
        Custom method that sets the current attribute of one Term object to
        True, and the rest False. Term objects in question are associated with
        the active-user.
        """
        user = self.request.user
        all_terms = user.terms.all()
        set_term = get_object_or_404(
            Term,
            user=user,
            session=current_term,
            )
        for term in all_terms:
            if term.current == True:
                term.current = False
            elif term == set_term:
                term.current = True
            term.save()

    def form_valid(self, form):
        """
        Form for setting the active-user's current term.
        """
        current_term_form = CurrentTermForm(self.request.POST)
        current_term = form.cleaned_data.get('current_term')
        self.set_current_term(current_term)
        return HttpResponseRedirect(self.success_url)

class UpdateTermView(UpdateView):
    """
    View that displays a form for updating an existing Term object.
    """
    template_name = 'update_term.html'
    form_class = TermForm
    success_url = reverse_lazy('Notes:term_edit')

    def get_object(self):
        """
        Retrieves object to be updated.
        """
        term = get_object_or_404(
            Term,
            term_slug=self.kwargs['slug'],
            user=self.request.user,
            )
        return term

    def get_context_data(self,**kwargs):
        """
        Provides extra context to the template for the purpose of turning the 
        'edit' button to a 'cancel edit' button
        """
        context = super().get_context_data(**kwargs)
        context['cancel_edit'] = True
        return context


class DeleteTermView(DeleteView):
    """
    View for deleting an existing Term object
    """
    success_url = reverse_lazy()

    def get_object(self):
        """
        Retrieves object to be deleted
        """
        term = get_object_or_404(
            Term,
            term_slug = self.kwargs['slug'],
            user = self.request.user,
            )
        return term


class CreateCourseView(CreateView, ListView):
    """
    View for creating a new Course object and listing all wxisting Course
    objects.
    """
    template_name = 'course_list.html'
    form_class = CourseForm
    context_object_name = 'courses'
    success_url = reverse_lazy('Notes:course')

    def get_queryset(self):
        """
        Retrieves all course objects associated with the active user.
        """
        active_user = self.request.user
        query_set = active_user.courses.all()
        return query_set

    def get_form_kwargs(self):
        """
        Passes the active-user to the form for the purpose of dynamically
        filtering term-choices to those associated with the active-user.
        """
        kwargs = super().get_form_kwargs();
        kwargs.update({'active_user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """
        Instantiates a new course object given the valid form.
        """
        course_form = CourseForm(self.request.POST)
        course = course_form.save(commit=False)
        course.user = self.request.user
        course.course_slug = slugify(course.course_code)
        course.save()
        return HttpResponseRedirect(self.success_url)


class CoursesOFTermView(CreateView, ListView):
    """
    View for creating a course object through a specific term as well as listing
    all Course objects associated with a specific Term object. 
    """
    template_name = 'course_list.html'
    context_object_name = 'courses'
    form_class = CoursesOfTermForm

    def get_success_url(self):
        """
        URl that directs a user to the courses of a specific term page.
        """
        args = [self.kwargs['slug']]
        return reverse_lazy('Notes:course_term', args=args)

    def get_queryset(self):
        """
        Retrieves Course objects associated with a specific term and 
        the active-user.
        """
        user = self.request.user
        term = get_object_or_404(
            Term,
            term_slug=self.kwargs['slug'],
            user=self.request.user,
            )
        slug = term.term_slug
        return Course.objects.filter(user=user, term__term_slug=slug)

    def get_context_data(self, **kwargs):
        """
        Provides extra context to the template
        """
        context = super().get_context_data(**kwargs)
        context['single_term'] = True
        slug = self.kwargs['slug']
        context['slug'] = slug
        subheader = slug[0].upper() + slug[1::]
        sub_header = ' '.join(subheader.split('-'))
        context['term_name'] = ': ' + sub_header
        return context

    def form_valid(self, form):
        """
        Instantiates a new Course object given the valid form.
        """
        course_form = CoursesOfTermForm(self.request.POST)
        course = course_form.save(commit=False)
        term = get_object_or_404(
            Term,
            term_slug=self.kwargs['slug'],
            user=self.request.user,
            )
        course.term = term
        course.user = self.request.user
        course.course_slug = slugify(course.course_code)
        course.save()
        return HttpResponseRedirect(self.get_success_url)


class UpdateOptionsCourse(ListView):
    """
    View for selecting to edit or delete a specific Course object
    """
    template_name = 'course_edit_delete.html'
    context_object_name = 'courses'

    def get_queryset(self):
        """
        Retrieves all Course objects associated with the active-user.
        """
        user = self.request.user
        queryset = user.courses.all()
        return queryset

    def get_context_data(self, **kwargs):
        """
        Provides extra context to the template.
        """
        context = super().get_context_data(**kwargs)
        context['editing'] = True
        return context


class DeleteCourseView(DeleteView):
    """
    View for deleting an existing course object.
    """
    success_url = reverse_lazy('Notes:course_edit')

    def get_object(self):
        """
        Retrieves to object to be deleted.
        """
        course = get_object_or_404(
            Course,
            user = self.request.user,
            course_slug = self.kwargs['slug'],
            )
        return course

    def get_success_url(self):
        """
        Generates the URL that the active-user is redirected to. If a course
        object is deleted within a specific term, the URL generated will direct 
        them to the course page of that aforementioned term; otherwise the URL
        that lists all courses will be generated
        """
        referer = self.request.META['HTTP_REFERER'].split('/')
        if referer[-2] == 'Edit':
            return reverse_lazy('Notes:course_edit')
        else:
            url_arg = [self.get_object().term.term_slug]
            return reverse('Notes:course_of_term_edit', args=url_arg)




