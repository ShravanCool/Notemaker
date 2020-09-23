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



