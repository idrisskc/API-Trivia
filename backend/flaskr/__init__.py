import os
from unittest import result
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_items(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories")
    def retrieve_categories():
        selection = Category.query.all()

        if len(selection) == 0:
            abort(404)

        result = {}
        for category in selection:
            item = category.format()
            result[item['id']] = item['type']

        return jsonify({'categories': result})

    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_items(request, selection)

        if len(current_questions) == 0:
            abort(404)

        selection = Category.query.all()

        if len(selection) == 0:
            abort(404)

        categories = {}
        for category in selection:
            item = category.format()
            categories[item['id']] = item['type']

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories,
                "current_category": categories[4]
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id
                }
            )

        except:
            abort(422)


    @app.route("/questions", methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        new_rating = body.get("rating", None)
        searchTerm = body.get('searchTerm')

        try:
            if searchTerm:
                result = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f'%{searchTerm}%')
                ).all()
                current_questions = paginate_items(request, result)
                return jsonify({
                    'questions': current_questions,
                    'total_question': len(result),
                    'success': True
                })
            else:
                question = Question(question=new_question,
                                    answer=new_answer,
                                    category=new_category,
                                    difficulty=new_difficulty
                                    )
                question.insert()

                return jsonify(
                    {
                        "created": question.id,
                        "success": True
                    }
                )

        except:
            abort(422)

    """
    TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }
            ),
            404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                }
            ),
            422
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 400,
                    "message": "bad request"
                }
            ),
            400
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 405,
                    "message": "method not allowed"
                }
            ),
            405
        )

    @app.errorhandler(500)
    def servererror(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 500,
                    "message": "internal server error"
                }
            ),
            500
        )

    return app
