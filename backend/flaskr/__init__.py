import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, all_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):

    ######################################################################
    # Initial setups
    ######################################################################

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """Set Access-Control-Allow"""

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
        categories = Category.query.order_by(Category.id).all()
        categories = [category.type for category in categories]

        return jsonify({
            'success': True,
            'categories': categories,
        })

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
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
            'total_questions': len(all_questions)
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
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

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_a_new_question():
        body = request.get_json()
        try:
            new_question = Question(
                question=body.get('question', None),
                answer=body.get('answer', None),
                category=body.get('category', None),
                difficulty=body.get('difficulty', None)
            )
            new_question.insert()

            all_questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, all_questions)

            return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': current_questions,
                'total_questions': len(all_questions),
            })

        except:
            abort(422)

    @app.route('/search_questions', methods=['POST'])
    def retrieve_questions_by_search():
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
            'current_category': list(categories),
            'total_questions': len(Question.query.all())
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
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

    @app.route('/quizzes', methods=['POST'])
    def retrieve_questions_for_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        print('previous_questions', previous_questions)
        print('quiz_category', quiz_category['type'])
        # print('Question.category', Question.category)

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
        print(questions_for_quiz)
        if len(questions_for_quiz) == 0:
            abort(404)

        question = random.choice(questions_for_quiz)

        return jsonify({
            "success": True,
            "question": question,
            "current_category": quiz_category
        })

    ######################################################################
    # Error Handlers
    ######################################################################

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request.",
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource is not found.",
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed.",
        }), 405

    @app.errorhandler(422)
    def unproceesable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable.",
        }), 422

    return app
