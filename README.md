# Trivia API

Description of project and motivation
Screenshots (if applicable), with captions

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
	  ]
}
```

#### GET /questions

- General: Retrieve a list of questions paginated by 10.
- Sample: `curl http://127.0.0.1:5000/questions`

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

#### DELETE /questions

- General: Delete a question with provided ID
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/5`

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

#### POST /questions

- General: Create a new question with provided data.
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H 'Content-Type: application/json' -d '{"question":"Test question","answer":"Test answer", "category":"1","difficulty":"1"}'`

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

#### POST /search_questions

- General: Retrieve questions which include provided searchTerm
- Sample: `curl -X POST http://127.0.0.1:5000/search_questions -H "Content-Type: application/json" -d '{"searchTerm": "Title"}'`

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

#### GET /categories/{int:category_id}/questions

- General: Retrieve all questions belonged to provided category.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

#### POST /quizzes

- General: Retrieve a random question which is in the provided category and not included in previous questions.
- Sample: `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [5, 9], "quiz_category": {"type": "History", "id": "4"}}`

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
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