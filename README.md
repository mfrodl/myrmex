# Myrmex
Interactive calendar for exercise tracking written in Django. [**Try it out!**](http://morning-brushlands-68412.herokuapp.com/exercise/)

Disclaimer
----------

These instructions have been hastily cobbled together by a Fedora user for other Fedora users. I hope to write a more comprehensive manual for people with other OS preferences in the future. In the meantime, consider this a take-home exercise. :smirk:

Prerequisites
-------------

:point_up: **All commands in this manual are to be run as `root`**

Myrmex is written in Python 3 using the Django web framework. Before you start, you should make sure they are installed on your system:

```
dnf -y install python3 python3-devel python3-pip gcc redhat-rpm-config
pip3 install django python-dateutil
```

Next, you will be needing a database backend. While several database management systems are supported by Django (and by extension, Myrmex), I recommend using MariaDB:

```
dnf -y install mariadb-server mariadb mariadb-devel
pip3 install mysqlclient
```

Finally, Django applications need a web server to run on. A common solution (and the one Myrmex has been developed on) is Apache HTTPD together with mod\_wsgi. So, let's install these as well:

```
dnf -y install httpd python3-mod_wsgi
```

Installation
------------

Currently, the only way to install Myrmex is to clone this Git repository on your machine. Again, I hope to make the installation more pleasant by using `setuptools` and ultimately pushing the package into [PyPI](https://pypi.python.org/), but for the time being, Git will have to do. If it is missing from your system, you will need to install it first:

```
dnf -y install git
```

We will clone the repository from GitHub to `/opt/myrmex`:

```
git clone https://github.com/mfrodl/myrmex.git /opt/myrmex
```

Database Setup
--------------

Start the database server and make it start automatically on system bootup:

```
systemctl start mariadb.service
systemctl enable mariadb.service
```

It is highly recommended to set the root password for MariaDB now (it it empty by default). Run the following command and enter new password when prompted to; for any other questions, you may answer `Y` (yes).

```
mysql_secure_installation
```

Now that the MariaDB environment has been set up, you will need to create a database for storing your exercise entries and a user that can access and manipulate the database. To do so, first log in to MariaDB's command-line client as `root` using the password you just generated:

```
mysql -p
```

In the client console, create the database and user by issuing the commands below. In this example setup, the database is named `myrmexdb`, the user has the login `myrmexuser@localhost` and the password `myrmexpassword`. Please don't take it too literally and **use different credentials**.

```mysql
CREATE DATABASE myrmexdb;
CREATE USER myrmexuser@localhost IDENTIFIED BY "myrmexpassword";
GRANT ALL PRIVILEGES ON myrmexdb.* TO myrmexuser@localhost;
QUIT;
```

For Myrmex to be able to access the database, we need to tell it which DBMS is used (MariaDB), where it resides (on local machine), what it is called (`myrmexdb`) and how to access it. In `/opt/myrmex/myrmex/settings.py`, edit the `DATABASES` variable as follows, replacing the credentials accordingly:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myrmexdb',
        'USER': 'myrmexuser',
        'PASSWORD': 'myrmexpassword',
        'HOST': 'localhost',
    }
}
```

Now that the database has been set up, we initialize it by running Django [migrations](https://docs.djangoproject.com/en/1.11/topics/migrations/):

```
cd /opt/myrmex
python3 manage.py migrate
```

Server Configuration
--------------------

Create file `/etc/httpd/conf.d/myrmex.conf` containing the below configuration.

```apache
WSGIScriptAlias / /opt/myrmex/myrmex/wsgi.py
WSGIPythonPath /opt/myrmex

<Directory /opt/myrmex/myrmex>
  <Files wsgi.py>
    Require all granted
  </Files>
</Directory>

Alias /media/ /opt/myrmex/exercise/media/
<Directory /opt/myrmex/exercise/media>
  Require all granted
</Directory>

Alias /static/ /opt/myrmex/exercise/static/
<Directory /opt/myrmex/exercise/static>
  Require all granted
</Directory>
```

Change SELinux context of the whole repository to allow HTTPD to access the files:

```
chcon -R -t httpd_sys_content_t /opt/myrmex
```

Start the web server and ensure it is started every time the system boots up:

```
systemctl start httpd.service
systemctl enable httpd.service
```

Test
----

Go to http://localhost/exercise and verify you can see this month's calendar.
