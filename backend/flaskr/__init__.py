"""Trivia Api

This application hold trivia on a regular basis and created a webpage
to manage the trivia app and play the game.

- Author: Mason Kim (icegom@gmail.com)
- Start code is provided by Udacity

Example:
    Execute "trivia api" for development environment

        $ FLASK_APP=flaskr FLASK_ENV=development flask run
"""
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, all_questions):
    """Paginate questions by QUESTIONS_PER_PAGE

    Args:
        request (obj): An instance of request_class
        all_questions (list): list of dictionaries which are json
            objects of all questions
    
    Returns:
        list: a paginated question list
    """
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    """create a Flask Application 'trivia_app'

    The main function of Trivia App.
    This function is consisted of three parts.
        - Initial setups
        - Endpoint functions
        - Error Handlers

    Args:
        test_config ():
    
    Returns:
        obj: a "Trivia API" Flask app object
    """

    ######################################################################
    # Initial setups
    ######################################################################

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """Setting Access-Control-Allow
        
        Args:
            response (obj): an instance of response_class
        
        Return:
            response object with Access-Control-Allow
        """
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, DELETE, OPTIONS'
        )
        return response

    ######################################################################
    # Endpoint functions
    ######################################################################

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        """An endpoint to handle GET requests '/categories'

        Handling GET requests for all available categories

        return
            json: a json object with 
                "categories": a list of all categories in database
        
        Raises:
            404: Resource is not found if there is no such a question.
            422: Unprocessable request.
        """
        try:
            categories = Category.query.order_by(Category.id).all()
            categories = [category.type for category in categories]

            if len(categories) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'categories': categories,
            })

        except Exception:
            abort(422)

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        """An endpoint to handle GET requests '/questions'

        Handling GET requests for questions, including pagination
        (every 10 questions).
        
        Return
            a json object with
                "questions": a list of pagenated questions
                "total_questions": the number of total questions
                "current_category": None
                "categories": a list of all categories' type
        
        Raises:
            404: Resource is not found if there is no such a question.
            422: Unprocessable request.
        """
        try:
            all_questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, all_questions)

            if len(current_questions) == 0:
                abort(404)

            categories = set()
            for question in current_questions:
                # categories.add(Category.query.get(question['category']).type)
                categories.add(question['category'])

            categories = Category.query.order_by(Category.id).all()
            categories = [category.type for category in categories]

            return jsonify({
                'success': True,
                'questions': current_questions,
                'categories': categories,
                'current_category': None,
                'total_questions': len(all_questions)
            })
        except Exception:
            abort(422)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """An endpoint to handle DELETE requests '/questions/<question_id>'

        Deleting a question matched with designated question ID.

        Args:
            question_id (int): The question id to delete

        return:
            A json object with
                "deleted": id of deleted question
                "questions": current_questions
                "total_questions": number of questions after deletion

        Raises:
            404: Resource is not found if there is no such a question.
            422: Unprocessable request.
        """
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            all_questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, all_questions)

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(all_questions),
            })

        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_a_new_question():
        """An endpoint to handle POST requests '/questions'

        Create a new question, which will require the question and
        answer text, category, and difficulty score.

        Return:
            A json object with
                "created": The id of newly created question
                "questions": A list of paginated questions
                "total_questions": The number of total questions

        Raises:
            422: Unprocessable request.
        """
        body = request.get_json()
        category_id = body.get('category', None)
        try:
            new_question = Question(
                question=body.get('question', None),
                answer=body.get('answer', None),
                category=category_id,
                difficulty=body.get('difficulty', None)
            )
            new_question.insert()

            all_questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, all_questions)
            category_type = Category.query.filter_by(category_id)

            return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': current_questions,
                'current_category': category_type,
                'total_questions': len(all_questions),
            })

        except Exception:
            abort(422)

    @app.route('/search_questions', methods=['POST'])
    def retrieve_questions_by_search():
        """An endpoint to handle POST requests '/search_questions'

        Get questions based on a search term. It should return any
        questions for whom the search term is a substring of the
        question. 

        Return:
            A json object with
                "questions": A list of paginated questions
                "current_category": None
                "total_questions": The number of total questions
        
        Raises:
            404: Resource is not found if there is no such a question.
            422: Unprocessable request.
        """
        try:
            body = request.get_json()
            search_term = body['searchTerm']
            questions_by_category = Question.query.filter(Question.question.ilike(
                f'%{search_term}%')).order_by(Question.id).all()
            current_questions = paginate_questions(request, questions_by_category)

            if len(current_questions) == 0:
                abort(404)

            categories = set()
            for question in current_questions:
                categories.add(Category.query.get(question['category']).type)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'current_category': None,
                'total_questions': len(Question.query.all())
            })

        except Exception:
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        """An endpoint to handle GET requests
           '/categories/<int:category_id>/questions'

        Create a GET endpoint to get questions based on category. 

        Args:
            category_id (int): The id of the category for seaching
                questions inclueded in it.

        Return:
            A json object with
                "questions": A list of paginated questions included in
                    the designated category
                "current_category": 
                "total_questions": The number of total questions
        
        Raises:
            404: Resource is not found if there is no such a question.
            422: Unprocessable request.
        """
        try:
            questions_by_category = Question.query.filter(
                Question.category == str(category_id)).order_by(Question.id).all()
            current_questions = paginate_questions(request, questions_by_category)

            if len(current_questions) == 0:
                abort(404)

            current_category = Category.query.get(category_id).type

            return jsonify({
                'success': True,
                'questions': current_questions,
                'current_category': current_category,
                'total_questions': len(Question.query.all())
            })

        except Exception:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def retrieve_questions_for_quiz():
        """An endpoint to handle POST requests '/quizzes'
        
        Getting questions to play the quiz. This endpoint should take
        category and previous question parameters and return a random
        questions within the given category, if provided, and that is
        not one of the previous questions. 

        Return:
            A json object with
                "question": A random questions within in the given category
                "current_category": Currently selected category
        
        Raises:
            404: Resource is not found if there is no such a question.
            422: Unprocessable request.
        """
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)

            # quiz_category 0 means 'all' categories
            # If so, questions can be selected from all categories.
            # Otherwise, select questions only from the selected category
            if quiz_category['id'] == 0:
                questions_for_quiz = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()
            else:
                questions_for_quiz = Question.query.filter(
                    Question.category == quiz_category['id'],
                    Question.id.notin_(previous_questions)
                ).all()

            questions_for_quiz = [
                question.format() for question in questions_for_quiz]
            if len(questions_for_quiz) == 0:
                abort(404)

            question = random.choice(questions_for_quiz)

            return jsonify({
                "success": True,
                "question": question,
                "current_category": quiz_category
            })
        except Exception:
            abort(422)

    ######################################################################
    # Error Handlers
    ######################################################################

    @app.errorhandler(400)
    def bad_request(error):
        """Error handler 400, Bas request"""

        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request.",
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        """Error handler 404, Resource is not found"""

        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource is not found.",
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Error handler 405, Method not allowed"""

        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed.",
        }), 405

    @app.errorhandler(422)
    def unproceesable(error):
        """Error handler 422, Unprocessable entity"""

        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable.",
        }), 422

    return app
