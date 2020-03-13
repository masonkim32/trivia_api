# Trivia API

The Trivia API is a Full Stack application that allows users to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game. The API is built in Flask, Javascript, and PostgresSQL.

All python modules in backends folder follows [PEP8 Style Guidelines](https://www.python.org/dev/peps/pep-0008/) and
Google [Python Docstring Guidelines](http://google.github.io/styleguide/pyguide.html).


## Getting Started

### Prerequisites & Installation

#### Prerequisites

- Python 3.6 or higher, and pip3
- Node, Git, and Postgresql
- Using python virtual environment is highly recommended.

#### Frontend Installation

To start the client, execute the following commands in the frontend folder:

```
npm install // only once to install dependencies
npm start
```

#### Backend Installation

Firstly, with Postgres running, restore a database using the trivia.psql file provided. From the backend folder
in terminal run:

```
psql trivia < trivia.psql
```

Install all required python modules in requirements.txt and set up local environment variables.
Then start flask project locally.

```
pip install requirements.txt
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Tests

To run tests, create the test database and run the python test script in the backend folder.

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference.

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Endpoints

#### GET /categories

- General: Retrieve a list of all categories.
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}
```

#### GET /questions

- General: Retrieve a list of questions paginated by 10.
- Sample: `curl http://127.0.0.1:5000/questions`

```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "current_category": null,
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

#### DELETE /questions

- General: Delete a question with provided ID
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/9`

```
{
  "deleted": 6,
  "success": true,
  "total_questions": 22
}
```

#### POST /questions

- General: Create a new question with provided data.
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H 'Content-Type: application/json' -d '{"question":"Test question","answer":"Test answer", "category":"1","difficulty":"1"}'`

```
{
  "created": 29,
  "current_category": "Science",
  "success": true,
  "total_questions": 25
}
```

#### POST /search_questions

- General: Retrieve questions which include provided searchTerm
- Sample: `curl -X POST http://127.0.0.1:5000/search_questions -H "Content-Type: application/json" -d '{"searchTerm": "What is"}'`

```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "success": true,
  "total_questions": 25
}
```

#### GET /categories/{int:category_id}/questions

- General: Retrieve all questions belonged to provided category.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
  ],
  "success": true,
  "total_questions": 25
}
```

#### POST /quizzes

- General: Retrieve a random question which is in the provided category and not included in previous questions.
- Sample: `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": ["2", "4"], "quiz_category": {"type": "Entertainment", "id": "5"}}'`

```
{
  "current_category": "Entertainment",
  "question": {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  "success": true
}
```

### Error Handling

- Errors are returned as JSON objects

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

- 400: Bad request
- 404: Resource is not found
- 405: Method not allowed
- 422: Unprocessable

## Authors

- Mason Myoungsung Kim
- Start Code provided by Udacity Team