Running the project
-------------------

Pre-requisites: Python, setuptools, pip and virtualenv

http://www.python.org/
http://pypi.python.org/pypi/setuptools
http://pypi.python.org/pypi/pip
http://pypi.python.org/pypi/virtualenv

Check out the code from GitHub.

$ cd sciencemuseum/sciexplore/

Create a virtualenv to install the dependencies:

$ virtualenv ve

Use pip to install the dependencies in to the virtualenv:

$ pip install -r requirements.txt -E ve

Run syncdb to create the database tables:

$ python manage.py syncdb

(You can answer "no" when asked if you want to create an admin account)

Next, import the data:

$ python manage.py import_xml http://www.sciencemuseum.org.uk/objectapi/cosmosculturepublic.svc/MuseumObjects

Now build the search index:

$ python manage.py rebuild_index

Finally, start up the development web server:

$ python manage.py runserver 8000

And load it in your browser:

http://localhost:8000/

