from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Term(models.Model):
	"""
	Display the academic year, term and link to courses view
	"""
	year = models.IntegerField(blank=False, null=True)
	term = models.CharField(max_length=40, blank=False)

	class Meta():
		"""
		Arranging in descending order of year
		"""
		ordering = ['-year']

class Courses(models.Model):
	"""
	Model to store the user's course name, course_id,
	terms and has link to notes view
	"""
	terms = models.ForeignKey(
		Term,
		on_delete=models.CASCADE,
		null=True,
		related_name='courses'
		)
	name = models.CharField(
		max_length=40,
		blank=False
		)
	course_id = models.CharField(
		max_length=40,
		unique=True,
		blank=False
		)

	class Meta():
		"""
		Ordering is done alphabetically according to
		course_id
		"""
		ordering = ['course_id']

# !!!Find usage of slugfield and sessions!!!


