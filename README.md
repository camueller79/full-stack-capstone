# FSND: Capstone Project

## Content

1. [Motivation](#motivation)
2. [Start project locally](#startlocal)
3. [API Documentation](#api)
4. [Authentification](#authentification)

<a name="motivation"></a>
## Motivation for project

This application was completed as the capstone project in the Udacity Full Stack Nanodegree course.
It covers the following technical topics that were explored throughout the course, such as:

1. Database modeling with `postgres` and `sqlalchemy` (in `models.py`)
2. Performing CRUD operations on a database with `Flask` (in `app.py`)
3. Automated testing with `Unittest` (in `test_app.py`)
4. Authorization and role based authentication with `Auth0` (in `auth.py`)
5. Deploying containerized applications on services such as `Heroku`

<a name="startlocal"></a>
## Start project locally

Make sure you are running an updated version of Python 3 as well as postgres

1. *optional* Initialize a virtual environment
    ```bash
    $ python3 -m venv env
    $ source venv/bin/activate
    ```
2. Install dependencies
    ```bash
    $ pip install -r requirements.txt
    ```
3. This application uses environment variables for dateabase url and auth0 config. Edit the setup.sh file and then activate it.
    ```bash
    $ source setup.sh
    ```
4. Run the application
    ```bash
    $ flask run
    ```
5. *optional* Test the application by running
    ```bash
    $ python3 test_app.py
    ```

<a name="api"></a>
## API Documentation

Here you'll find documention on all end points and supported methods, as well as role based permissions needed for each.

### Base URL
**_https://camueller-capstone.herokuapp.com_**

### Roles and keys

The entire application is unavailable without the permissions offered by one or two roles. 

1. Read Only - you'll find the auth key for this role in setup.sh as variable READONLY_KEY
    1. RBAC permissions: get:albums, get:bands
2. Manager - you'll find the auth key for this role in setup.sh as variable MANAGER_KEY
    1. RBAC permissions: get:albums, get:bands, post:album, post:band, patch:album, patch:band, delete:album, delete:band

### Endpoints

#### GET /bands
requires_auth(get:bands)
returns json object list of bands

#### GET /albums
requires_auth(get:albums)
returns json object list of albums

#### POST /bands/add
requires_auth(post:band)
takes a json object of a band in the format 
```bash
{
    'name': 'band_name',
    'city': 'some city',
    'state': 'MO'
}
```
and returns a json object like this:
```bash
{
    'success': True,
    'band': {
        'name': 'band_name',
        'city': 'some city',
        'state': 'MO'
    }
}
```

#### POST /albums/add
requires_auth(post:album)
takes a json object of an album in the format 
```bash
{
    'title': 'album_title',
    'band_id': int
}
```
and returns a json object like this:
```bash
{
    'success': True,
    'album': {
        'title': 'band_name',
        'band_id': int
    }
}
```

#### DELETE /bands/<int:band_id>
requires_auth(delete:band)
takes a band id via the url and returns json object in this format:
```bash
{
    'success': True,
    'band_id': int
}
```

#### DELETE /albums/<int:album_id>
requires_auth(delete:band)
takes an album id via the url and returns json object in this format:
```bash
{
    'success': True,
    'album_id': int
}
```

#### PATCH /bands/<int:band_id>
requires_auth(patch:band)
takes a band id via the url and a json object of a band in the format 
```bash
{
    'name': 'band_name',
    'city': 'some city',
    'state': 'MO'
}
```
and returns a json object in this format:
```bash
{
    'success': True,
    'band': {
        'name': 'band name',
        'city': 'city name',
        'state': 'MO'
    }
}
```

#### PATCH /albums/<int:album_id>
requires_auth(patch:album)
takes an album id via the url and an album in the following json format:
```bash
{
    'title': 'album_title',
    'band_id': int
}
```
and returns a json object in this format:
```bash
{
    'success': True,
    'band': {
        'name': 'band name',
        'city': 'city name',
        'state': 'MO'
    }
}
```
