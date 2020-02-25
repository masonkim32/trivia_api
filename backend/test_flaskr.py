import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'trivia',
            'development',
            '172.17.0.2:5432',
            self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) <= 10)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_sent_requesting_beyond_valid_page(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource is not found.')

    @unittest.skip("test delete for just one time")
    def test_delete_question(self):
        total_num_of_questions_before_delete = len(Question.query.all())
        response = self.client().delete('/questions/5')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(data['questions'])
        num_of_deleted_question = \
            total_num_of_questions_before_delete - data['total_questions']
        self.assertEqual(num_of_deleted_question, 1)

    def test_404_sent_deleting_non_existing_question(self):
        response = self.client().delete('/question/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource is not found.')

    def test_add_a_new_question(self):
        total_num_of_questions_before_add = len(Question.query.all())
        new_question = {
            "question": "new question",
            "answer": "an answer for new question",
            "difficulty": "2",
            "category": "3",
        }
        response = self.client().post('questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        num_of_added_question = \
            data['total_questions'] - total_num_of_questions_before_add
        self.assertEqual(num_of_added_question, 1)

    def test_search_question(self):
        search = {
            "searchTerm": "What is"
        }
        response = self.client().post('search_questions', json=search)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['total_questions'])

    def test_405_sent_searching_question_with_get_method(self):
        search = {
            "searchTerm": "What is"
        }
        response = self.client().get('search_questions', json=search)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method not allowed.')

    def test_get_questions_by_category(self):
        response = self.client().get('categories/5/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'] == "Entertainment")

    def test_get_random_question_for_quizzes(self):
        response = self.client().post(
            'quizzes',
            data=json.dumps({
                "previous_questions": ['13'],
                "quiz_category": "3"
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['current_category'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
