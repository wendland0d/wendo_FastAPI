# wendo_FastAPI
made by @wendo as Test-case Junior Python Developer
## How to run
This case is based on FastAPI uses Docker-Compose as a containerization system for work. Actually, to run it, you will need to install Docker and Docker-Compose on your server or work machine. The easiest way is presented in the form of official documentation on the website https://docs.docker.com/desktop/. After installing Dokker and Docker-Compose, you can start deploying the API.

1. Step one - you need to download (clone) the repository to your server - use the following command 

```git clone git@github.com:wendland0d/wendo_FastAPI.git```

2. Step two - after you have successfully cloned the repository, you need to go to the repository folder using the command

```cd wendo_FastAPI/```

3. Step three - you can immediately start the service using the command

```docker-compose up -d```

And also optionally change the environment variables. To do this, you need to open the file ```docker-compose.yaml``` using any editor available to you (Nano, Vim etc)
## What does API use for work
After deploy API starts on UVICORN and uses ```3112``` port (You can change it in ```docker-compose.yaml```)
## API Docs
API is automatically generate OpenAPI docs in Swagger. For checking and exporting OpenAPI docs you can go to ```<your-ip>:3112/docs``` and use it whatever you want!
If you want to try it by youself you also can use Swagger as web-client or Postman (i decided to use Postman because its pretty simple to start and very usefull to help you when you building you own API)

## TO-DO
- [x] Docker-compose based and running
- [ ] Debug all pydantic models and review code-style
- [ ] Unit-tests 
- [ ] CI/CD integration

## Divergencies from the terms of reference
Thanks to a competently constructed technical task, I did not have to "design a bike", but I decided to make some changes:

1. Added the possibility of self-registration of users - this will help you test the API faster with your own hands.
2. I used PostgreSQL as a system for storing user information. PostgreSQL is one of the most popular DBMS and since almost all my experience with SQL is related to Postgres, I decided to use it. PostgreSQL is run by a separate container together with the API, and therefore you do not need to perform additional manipulations with installing and configuring it locally on the server.

## Is it works somewhere now?
Yes, it works! It's already running on my server and ready to try! I can't provide here an address of server due probability of spam or ddos-attacks. If you want to try it without deploying it whenever - just PM me in telegram and we can talk about it!
