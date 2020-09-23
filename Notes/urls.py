#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import (CreateTermView, CreateCourseView, CoursesOfTermView, 
                    CreateNoteView, NotesList, NotesOfCourse, ReadNote,
                    UpdateOptionsTerm, DeleteTermView, UpdateTermView,
                    UpdateOptionsCourse, DeleteCourseView,
                    CoursesOfTermEditView, UpdateCourseView, NoteUpdateOptions,
                    NotesOfCourseUpdateOptions, DeleteNoteView, UpdateNoteView,
                    SearchBar, NotesListSearchQuery, )

app_name = 'Notes'

urlpatterns = [
    path(
        'Courses/All-Notes/',
        login_required(NotesList.as_view()),
        name = 'notes_list',
        ),
    path(
        'Courses/<notes_query>/',
        login_required(NotesListSearchQuery.as_view()),
        name = 'notes_search',
        ),
    path(
        'Courses/All-Notes/Edit/',
        login_required(NoteUpdateOptions.as_view()),
        name = 'note_edit',
        ),
    path(
        'Courses/All-Notes/Edit/Delete/<created_at>/',
        login_required(DeleteNoteView.as_view()),
        name = 'note_delete',
        ),
    path(
        'Courses/SingleCourse/<slug>/',
        login_required(CoursesOfTermView.as_view()),
        name = 'course_term',
        ),
    path(
        'Course/Edit/<slug>/',
        login_required(CoursesOfTermEditView.as_view()),
        name = 'course_of_term_edit',
        ),
    path(
        'Course/Edit/Update/<slug>/<single_term>/',
        login_required(UpdateCourseView.as_view()),
        name = 'course_update',
        ),
    path(
        'Courses/<slug>/<course_id>/',
        login_required(NotesOfCourse.as_view()),
        name = 'notes_of_course',
        ),
    path(
        'Courses/<slug>/<course_id>/Edit/',
        login_required(NotesOfCourseUpdateOptions.as_view()),
        name = 'notes_of_course_edit',
        ),
    path(
        'Courses/<slug>/<course_id>/<note_slug>/',
        login_required(ReadNote.as_view()),
        name = 'one_note',
        ),
    path(
        'Courses/<slug>/<course_id>/<note-slug>/Edit/',
        login_required(UpdateNoteView.as_view()),
        name = 'update_note',
        ),
    ]
