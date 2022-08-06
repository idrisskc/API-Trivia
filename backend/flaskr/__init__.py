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
        searchTerm = body.get('searchTerm')

        try:
            if searchTerm:
                result = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f'%{searchTerm}%')
                ).all()
                current_questions = paginate_items(request, result)

                selection = Category.query.all()

                if len(selection) == 0:
                    abort(404)
                categories = {}
                for category in selection:
                    item = category.format()
                    categories[item['id']] = item['type']

                return jsonify({
                    'questions': current_questions,
                    'total_questions': len(result),
                    'current_category': categories[4],
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

    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def retrieve_category_questions(category_id):
        category = Category.query.filter(
            category_id == Category.id).one_or_none()

        if (category is None):
            abort(404)

        try:
            selection = Question.query.filter(
                Question.category == category.id).all()
            current_questions = paginate_items(request, selection)

            return jsonify({
                'questions': current_questions,
                'current_category': category.type,
                'total_questions': len(selection)
            })

        except:
            abort(404)

    @app.route("/quizzes", methods=['POST'])
    def retreive_next_quizz():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            category_id = quiz_category['id']

            questions = Question.query.filter(Question.id.notin_(
                previous_questions), Question.category == category_id).all()

            if(questions):
                question = random.choice(questions)

            return jsonify({
                'question': question.format()
            })

        except:
            abort(422)


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
