# Basketball Team and Player Management API

![image](https://github.com/VianaCoder/basketball-manager/assets/45436876/ce25f3c3-a151-4f38-a0db-e28841c41e6a)

This API was developed to manage information about basketball teams, players, and related games. It allows operations such as creating, updating, viewing, and deleting records of teams, players, and games.

## Technologies Used

- Django: Web framework used for developing the API.
- Django REST Framework: Django extension that facilitates building RESTful APIs.
- SQLite: Lightweight database used to store application data.

## Key Features

- **Teams:**
  - List all teams.
  - Create, view, update, and delete teams.
  - Assign a coach to a team.

- **Players:**
  - List all players.
  - Create, view, update, and delete players.
  - Assign a player to a specific team.

- **Games:**
  - List all games.
  - Create, view, update, and delete games.
  - Record game results.

- **Authentication:**
  - Token-based authentication to protect sensitive endpoints.
  - User profiles: administrator and coach.

## Available Endpoints

### Teams

- **GET /teams/**: Retrieve all teams.
- **POST /teams/**: Create a new team.
- **GET /teams/{id}/**: Retrieve details of a specific team.
- **PUT /teams/{id}/**: Update information of a team.
- **DELETE /teams/{id}/**: Delete a team.

### Players

- **GET /players/**: Retrieve all players.
- **POST /players/**: Create a new player.
- **GET /players/{id}/**: Retrieve details of a specific player.
- **PUT /players/{id}/**: Update information of a player.
- **DELETE /players/{id}/**: Delete a player.

### Games

- **GET /games/**: Retrieve all games.
- **POST /games/**: Create a new game.
- **PUT /games/{id}/**: Update information of a game.
- **DELETE /games/{id}/**: Delete a game.

### Authentication

- **POST /login/**: Endpoint to obtain authentication token (username and password).
- **POST /user/**: Create a new user (administrator or coach).

### Installation:

##### - Create your virtual enviroment

##### - Active your enviroment

##### - Install required dependencies:
``` cd api ```
``` pip install -r requirements.txt ```

##### - Setup the database:
``` python manage.py makemigrations ```
``` python manage.py migrate ```

##### - Run the server:
``` python manage.py runserver ``` 

##### - Set the variables to populate data:
``` export DJANGO_PROJECT_PATH="/path/to/the/project" ```
``` export DJANGO_SETTINGS_MODULE="api.settings" ```

##### - Run the populate script:
``` python \scripts\populate_database.py ```

### Python Version 
Python 3.10.12
