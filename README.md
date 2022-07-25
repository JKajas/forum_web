# forum_web

## Description
Application gives you a simple tools to create your own forum. You can create users, organizations, articles and comment them. 

## Technologies 

- Django 4.0.5
- Celery 5.2.7
- mysqlclient 2.1.1
- django-ckeeditor
- crispy-bootstrap5

## Get started 

Application is ready to work in fully virtual environment. It requires configured mySQL database and broker RabbitMQ.
If you want run it with docker follow this steps: 
1. Pull image of mySQL and configure it. By default application forum_web uses three environment variables to connect to database:
- MYSQL_DATABASE= mysqlDB
- MYSQL_USER=root
- MYSQL_ROOT_PASSWORD=rootpassword </br></br>
You need to create them during run image. Give container name "db". It will be required to link him to application container.
~~~
docker pull mysql:latest
~~~
~~~
docker run --name db -e MYSQL_DATABASE=mysqlDB -e MYSQL_ROOT_PASSWORD=rootpassword mysql:latest 
~~~
2. Now you should pull RabbitMQ image and run it with default configuration. Give container name "broker". It will be needed to link him to application container.
~~~
docker pull rabbitmq:3.10-management
~~~
~~~
docker run --name broker rabbitmq:3.10-management
~~~
3. Now pull app image. You can see in on https://hub.docker.com/repository/docker/jkajas/forum_web.
~~~
docker pull jkajas/forum_web:latest
~~~
4. Link other containers(db and broker) to application container and create volume to manage for example email saving backend. Work dir has name "/forum". If you want to have access to emails you should set a path for example "/forum/emails".
If you want to have access to media you should set a path for example "/forum/emails".
~~~
docker run --name web -v <your_path>:/forum/emails --link db:db --link broker:broker jkajas/forum_web:latest 
~~~
5. During every start container does migration to database, run server and starts celery worker.</br> 
6. Now you are ready to work. You can connect to the app by container ip.
~~~
http://<container-ip>:8000/
~~~
## How does it work?

- **Configuration**</br> 
  * File `settings.py` has indicated configuration require to easy run container and celery module.</br>
  * `ALLOWED_HOST` takes always ip of the container by socket module.</br>
  * `CELERY_BROKER_URL` has linked name of broker container. As it was mensioned before, you should create container with this name.</br>
  * `DATABASES` has also linked name of db container. Additionally takes environment varaibles given during building container. You should create this variables in mySQL database first. </br>
 - **Celery**</br>
 * Celery is created in `celery.py`. It autodiscovers tasks in `tasks.py`. In app exist one scheduled task, preformed every second.</br>
 * Celery works asynchronus so it doesn't influence application code running. Task does operations on database that app takes data from.
 
## Application features 

- **Create user** </br>
  You can create two types of user. User and his proxy model - organization user. Register them by yourself getting template sign up or create them using admin panel. 
  Application has customized admin model and commands that can create super users for each type of user. Simply type inside the container:
  ~~~
  python3 manage.py createorgadm
  ~~~
- **Wide authenthication system**</br>
  You can use customized authentication system. If someone is organization member you don't need to log in by entire email but only with alias.  
- **Add article and comment them!**</br>
  * Create article on your profile site. 
  * Browse other user's articles
  * Share comments below article you like 
- **Reset password if you forgot** </br>
  Simple reset password system working with celery. Request generate token for url to reset password. Celery check token if it isn't too long in database and if it is immidetely delete him. 
 - **More back-end**</br>
   * Three simple middlewares who watch if you reach that endpoint you should reach or helps you to find contets throught search bar 
   * Simple unit tests checking basic factors of application
   * Validators don't allow you to create exist user with password which have been leaked. Also validators control length of words or types of characters.

## What's next
In near future project will be hosted on Cloud server. I will focus on seeking bugs and fixing them. 

