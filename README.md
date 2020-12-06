# NoteMaker

NoteMaker is a note-taking web application, using which students can efficiently take notes, access them, categorise them to proper courses, terms, years, and schools.

Check out the [application](https://demo-notemaker.herokuapp.com) deployed in heroku.

## Why?

Throughout my undergraduate course, I was exposed to a panomaly of different note-taking applications, the one I found myself most frequently using was [Google Docs](https://docs.google.com/document/u/0/). Google Docs though powerful in the capabilities of its rich text editor, doesn't offer an ease with which to organize saved notes into an intuitive structure. I wanted to add an extra layer to organization in so far as to giving the user the ability to organize not just their notes but also courses, academic terms, year, and school. Though people can just as easily attain a high degree of organization via nested directories on their desktop, I wanted something that was more dynamic, and hence I created **Notemaker**.

## Features-

- Take notes using mark-down editor, which enables them to type and arrange their notes very efficiently.
- Access notes easily by entering the title in the search bar.
- Allow access and	interact with the application's web-browsable API from the dashboard.

## Built with-

- [Bootstrap](https://getbootstrap.com/)- Frontend Framework
- [Django-mdeditor](https://github.com/pylixm/django-mdeditor)- Rich Text-editor with Markdown support and preview
- [Django](https://www.djangoproject.com/)- Backend Framework
- [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)- Control over form rendering behaviour
- [Django Rest Framework](https://www.django-rest-framework.org/)- Web-browsable API
- [JQuery](https://jquery.com/)- Event listeners
- [SQLite3](https://www.sqlite.org/index.html)- Database

## Directions for Setting up Environment-

To install the source, pre-requisites include-

- Python 3.6 or above
- Dependencies from requirements.txt

First, clone this repository onto your system. Then, create a virtual environment:

```
cd path/to/folder
virtualenv venv -p python3.6  //or any other name and version
source venv/bin/activate
```

Now, install the python dependencies from requirements.txt:
```
pip install -r requirements.txt
```

The next step is to set your environment variables in .venv file (otherwise hardcode the string `SECRET_KEY` in Notemaker/settings.py) and also modify the `ALLOWED_HOSTS` in Notemaker/settings.py.
```
##App variable
SECRET_KEY=SomeRandomStringOfText
DEBUG=True
ALLOWED_HOSTS=.localhost,127.0.0.1
```

Lastly, build the database by making migrations:
```
python manage.py makemigrations
python manage.py migrate
```

## Directions to execute-

Inside the main project directory (the directory with the 'manage.py' file), run the following command to start the server-
```
python manage.py runserver
```

Now open the link shown in the terminal in any browser of your choice.
