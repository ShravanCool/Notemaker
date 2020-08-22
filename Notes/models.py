from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model 

# Create your models here.
class Term(models.Model):
        """
        Display the academic year, term and link to courses view
        """
        user = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE,
            related_name='terms',
            )
        year = models.IntegerField(blank=False, null=True)
        session = models.CharField(max_length=40, blank=False)
        term_slug = models.SlugField(max_length=40, blank=False)
        current = models.BooleanField(default=False)

        def __str__(self):
            """"
            Provides a readable string representation of Term object
            """
            return f'{self.session}'

        class Meta():
            """
            Arranging in descending order of year
            """
            ordering = ['-year']

class Course(models.Model):
        """
        Model to store the user's course name, course_id,
        terms and has link to notes view
        """
        user = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE,
            related_name='terms',
            ) 
        term = models.ForeignKey(
            Term,
            on_delete=models.CASCADE,
            null=True,
            related_name='courses'
            )
        course_code = models.CharField(
                max_length=40,
                unique=True,
                blank=False
                )
        title = models.CharField(max_length=40, blank=False)
        course_slug = models.SlugField(null=True)

        def __str__(self):
            """
            Provides a readable string representation of Course object
            """
            return f'{self.course_code}'

        class Meta():
                """
                Ordering is done alphabetically according to
                course_id
                """
                ordering = ['course_id']

class ClassNote(models.Model):
    """
    Model whos objects are the actual notes that the user takes. Each ClassNote 
    object is related to a specific user in their course.
    """
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='terms',
        ) 
    title = models.CharField(max_length=40, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    body= RichTextField(config_name='ckeditor')  #Modify to Markdown!!!
    note_slug = models.SlugField(null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        related_name='notes'
        )

    def __str__(self):
        """
        Provides a readable string representation of ClassNote object
        """
        return f'{self.title}'

    def join_title(self):
        """
        Uses a ClassNote object's title to produce a lowercased version devoid of
        whitespaces and returns as string
        """
        joined_title = ''.join(self.title.lower().split(' '))
        return joined_title

    class Meta():
        """
        Orders ClassNote objects first by their courses alphabetically, objects with
        the same course are then ordered by most recent
        """
        ordering = ['course', '-created_at']


