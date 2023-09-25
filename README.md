# Jira-rest-api

### Python application run command
 ```
 python3 -m flask run
```

### Docker container up and running 
```
docker build . -t jira-api
```
```
docker run -p 8089:4000 -d jira-api # run image file
```

### docker hub upload an image
 ```
 docker ps
```
```
docker commit 87abc1b8aeb3 jira_rest_api:latest
```
# before login create a reporsitory in dockerhub
- docker login # set userid and password of dockerhub account
- ```docker tag jira_rest_api:latest lota123/jira-automate-report:latest```
- ```docker push lota123/jira-automate-report:latest```

![Screenshot from 2023-04-06 10-58-58](https://user-images.githubusercontent.com/23186076/230275936-4388c5e6-f4d1-4d67-988a-9b77f0b5f52d.png)

### pull from docker and run in local
- ```docker pull lota123/jira-automate-report:latest```
- ```docker run -it lota123/jira-automate-report:latest```

![Screenshot from 2023-04-06 11-11-25](https://user-images.githubusercontent.com/23186076/230277545-5d8028ca-abbe-420f-b5f7-aecde7dbe361.png)
