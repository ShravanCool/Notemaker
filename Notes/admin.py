from django.contrib import admin
from .models import Term, Course, ClassNote

# Register your models here.
admin.site.register(Term)
admin.site.register(Course)
admin.site.register(ClassNote)
