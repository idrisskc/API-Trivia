# API Trivia

Udacity s'investit dans la création de liens pour ses employés et ses étudiants. Des membres de l'équipe ont eu l'idée de maintenir Trivia et ont créé une page Web pour gérer l'application Trivia et jouer le jeu, mais leur expérience API est limitée et doit encore être construite. Ce projet donne leur donne la possibilité de planifier, d'implémenter et de tester une API.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Student Guidelines

Hello students! You'll use this base in various workspaces throughout the course to build the project incrementally as you expand your skills. At each stage, there will be various 'TODO's marked for you to complete. You'll also notice some TODOs in the frontend section. You should referene those sections for formatting your endpoints and responses, and update the frontend to match the endpoints you choose and the programmed behavior. 

You should feel free to expand on the project in any way you can dream up to extend your skills. For instance, you could add additional book information to each entry or create individual book views including more information about the book, your thoughts or when you completed it. 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error 

### Endpoints 
#### GET /categories
- General:
    
    - Récupère un dictionnaire de catégories dans lequel les clés sont les ID, et la valeur est la chaîne correspondante de la catégorie
    - Arguments de la requête : aucun
    - Retourne : objet avec une seule clé, « categories », qui contient un objet « id : category_string » : paires de valeurs.
 
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```
#### GET /questions
- General:
    - Returns a list of questions objects, success value, and total number of questions, current_category, categories
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "History", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```
#### POST /questions
- General:
    - Envoie une requête POST afin d'ajouter une nouvelle question

- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question":  "Here is a new question chain","answer":  "Here is a new answer string","difficulty": 1,"category": 3}'`
```
{
  "created": 25, 
  "success": true
}
```

#### POST /questions
- General:
    -Envoie une requête POST afin de rechercher une question spécifique par terme de recherche

- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'`
```
{
  "current_category": "History", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

#### DELETE /questions/{question_id}
- General:
  - Supprime une question spécifiée en utilisant l'identifiant de la question
  - Arguments de la requête : « id » - entier
  - Retourne : il n'est pas nécessaire de retourner autre chose que le code d'état HTTP approprié. Il est possible de renvoyer l'ID de la question. Si vous êtes en mesure de modifier le front-end, vous pouvez lui faire supprimer la question en utilisant l'id au lieu de récupérer les questions
- `curl -X DELETE http://127.0.0.1:5000/questions/16`
```
{
  "deleted": 16, 
  "success": true
}
```

#### GET /categories/{category_id}/questions
- General:
  - get questions based on category
  - Arguments de la requête : « category_id » - entier
  - Retourne : questions based on category
- `curl -X GET  http://127.0.0.1:5000/categories/5/questions`
```
{
  "current_category": "Entertainment", 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "total_questions": 2
}
```

#### POST /quizzes
- General:
    - Envoie une requête POST afin d'obtenir la prochaine question

- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [],"quiz_category": {"type": "Entertainment", "id": 5}}'`
```
{
  "question": {
    "answer": "Edward Scissorhands", 
    "category": 5, 
    "difficulty": 3, 
    "id": 6, 
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }
}
```


## Deployment N/A

## Authors
FOKOU Arnaud Cedric
