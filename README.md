# images-project

## Main Technologies
* Python 3.9
* Django 4.0.5
* Django REST framework 3.13.1
* Pillow
* restframework-serializer-permissions 0.0.2


## Installation

### Clone the GitHub repository to your directory.

```bash
git clone https://github.com/adrianbuskiewicz/images-project.git
```

### Go into the directory and use docker-compose.

```bash
cd images-project
docker-compose up
```

### Add bultin account tiers.
```bash
docker exec -it <container_id> python manage.py loaddata tier.json
```

### Create superuser.
```bash
docker exec -it <container_id> python manage.py createsuperuser
```
### After creating a superuser remember to give him a tier if you want to use him as a normal user!


## Usage of REST API

### App uses standard DRF SessionAuthentication and TokenAuthentication (including the token in headers is necessary).

`Authorization: Token <user_token>`


### GET method for receive all images uploaded by user.
`GET /api/`
```bash
curl -H "Authorization: Token <user_token>" http://127.0.0.1:8000/api/
```


### POST method for uploading images by user
`POST /api/upload/`

Parameters in body:
- #### title
- #### original_image



### POST method for creating an expiring link to the image
`POST /api/create_link/`

Parameters in body:
- #### img_id
- #### seconds


## Testing in root directory (images-project).
```bash
pytest
```
