# Simple instructions for impatients users
---
\
These simple steps guides you trough a simple way to test/install Ticketator on a common scenario, as could be a Debian 8 server.

### Using standalone Django server (only for testing)



```sh
apt-get install python-pip postgresql git python-psycopg2
```
-create a user if you want (by ex. "django")

-change to this user

```sh
git clone https://github.com/sabueso/ticketator.git
```

-as postgres user, "cd /home/django/ticketator/utils/" & "./1_create_database.sh"

-as root

```sh
pip install -r requirements.txt 
``` 

(if you don't do as root, hangs in some part, i have to review that ASAP)

-as django user, "./manage.py makemigrations; ./manage.py migrate"

-as django user, "./manage.py createsuperuser"

-Now, to populate some needed data from the base directory of the instalation:

```sh
./manage.py loaddata fixtures/1_states.json 
./manage.py loaddata fixtures/2_usertypes.json 
./manage.py loaddata fixtures/3_priority.json 
```

-Now, you can load the microwebserver that comes with Django from your normal user:
```sh
./manage.py runserver <you_desired_ip>:8080
```
or if you want to use it from localhost
```sh
./manage.py runserver
```

###  Using with Apache2

Install Ticketator on Apache is quite simple. Inside "util" directory, you could find a virtualhost file example to use apache with WSGI, in order to execute Ticketator Python code.

In simple steps:

```sh
apt-get install libapache2-mod-wsgi
``` 

Then, clone the repo, install the requerimentes

Now, you can situate the virtualhost file located under "util" directory inside /etc/apache2/sites-avaliable, make the symlink to enable in configuration and testing it.

Virtualhost file may look similar to this one:

```sh
Listen 80

<VirtualHost *:80>

ServerAdmin you@yourdoain.com
ServerName host.domain.com

WSGIScriptAlias / /var/www/ticketator/ticketator/wsgi.py process-group=ticketator
WSGIDaemonProcess  ticketator processes=5 threads=10 display-name=%{GROUP} python-path=/var/www/ticketator
WSGIProcessGroup ticketator


Alias /media/ /var/www/ticketator/media/
Alias /static/ /var/www/ticketator/static/


<Directory /var/www/ticketator/ticketator>
	<Files wsgi.py>
	Require all granted
	</Files>
</Directory>

</VirtualHost>
```

Adjust all to fit in to your Apache2 config.

##### Some considerations about the code execution & Apache2:

In order to avoid problems with uploaded files & perms, we recommend to situate the code of ticketator under /var/www.
Once did that, remember to change the ownership of the code repository to "www-data" user&group.

### Warning
If you won't do that, you can situate the code in other path, and adjust the virtualhost fiel to point to that path, but maybe, thats not the better choice to run code under a webserver and some missconfiguration could carry security problems.
You're warned.


# Further common steps to all installation methods:

Logged as and admin

* Create a Company
* Create groups
* Create users
* Create some queue
* Create rights for those groups <=> queues
* Make your first ticket ;)

Now enjoy and give constructive feedback! ;)

Ramiro (ramiro@ticketator.org)