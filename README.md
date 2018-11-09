# computrabajo-bot
Static website and django project to login and apply automatically to all job offers listed in computrabajo.com.mx

## Usage
Go to the https://wallee94.github.io/computrabajo-bot/ and submit the form using your computrabajo.com.mx credentials and query. 
No data is stored in any database and some values related to the user, like session cookies are only stored while tha task
is running.

The program is free to use and comes as it is, with no waranty that it will work 24/7 or that it won't stop running in the future.
Feel free to pull request any fix you find or to fork the project to your own repo.

## Docker
The django project runs using docker-compose, with a local and a production environment. The main difference is that the 
prod docker-compose will try to setup a caddy server and run the django project using gunicorn instead of the `runserver` command.

To run in you own server, download this repo, install docker and docker-compose and run:

    sudo docker-compose -f production.yml up -d
    
Also, create a `.envs/.production/.caddy` and `.envs/.production/.django` file to setup your environ variables, 
like caddy's DOMAIN_NAME.
    
To run locally change `production.yml` for `local.yml`.
You'll probably have to setup some environ variables like a mailgun private api key to make it work locally.
