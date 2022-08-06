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
        self.database_path = "postgres://{}/{}".format(
            'postgres:fokou2014@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question':  'Here is a new question title',
            'answer':  'Here is a new answer string',
            'difficulty': 1,
            'category': 3,
        }
        self.new_search={'searchTerm': 'title'}
        self.quiz_param = {'previous_questions': [],'quiz_category': {'type': 'Entertainment', 'id': 5}}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))

    def test_delete_question(self):
        res = self.client().delete("/questions/6")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 6)
        self.assertEqual(question, None)

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
      
    def test_search_questions(self):
        res = self.client().post('/questions', json=self.new_search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertEqual(data['success'], True)

    def test_get_questions_per_category(self):
        res = self.client().get(f'/categories/{6}/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_get_next_quiz(self): 
        res = self.client().post('/quizzes', json=self.quiz_param)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
       

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
