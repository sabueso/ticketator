# Ticketator

Ticketator is a simple ticketing system developed in Python 2, based on Django Framework.
It's inspired in some Jira features and others ticketing systems commonly used by IT Departments.

![alt tag](https://dl.dropboxusercontent.com/u/13983419/index.png)

Ticketator is about tickets, queues, users and groups.

###Some cool features

* Simple ticket creation
* Queus to organize tickets
* Rights to organize access to queues (based on group access, can comment, can edit, can view...)
* Comments on tickets
* Ability to define percentage made on a particular task
* Multiple users and groups
* HTML responsible design
* Only a few AJAX calls, not a Javascript/Jquery monster

Start to use Ticketator is as simple as install it, load initial data, create a superuser, a queue, and you're ready to create tickets!

Give a try to Ticketator, and give us your feedback!


### Dependencies

* [Django] 1.9 or greater
* Postgres or similar (as supported by Django ORM)
* [django-colorfield] 
* [django-extensions] 

### Installation
```sh
git clone https://github.com/sabueso/ticketator.git
```
Once installed, satisfy some dependencies manually
```sh
pip install django-colorfield
pip install django-extensions
```
TODO: first steps to put Ticketator on road.

### Docker demo
Docker image to test Ticketator without effort
```sh
TODO:
```
### Disclaimer

Ticketator is under active developement and some areas could not be working as expected. Please, let you free to comment it constructively under the "Issue" area on Github.

### Todos

 - Write Tests
 - Create more consisten logs for tickets
 - A lot of more things

License
----
TODO


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [Django]: <https://www.djangoproject.com/download/>
