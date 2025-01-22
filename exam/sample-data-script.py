from django.core.management.base import BaseCommand
from exam.models import Course, Question
from django.contrib.auth.models import User, Group
from student.models import Student
import random

class Command(BaseCommand):
    help = 'Adds sample courses and questions to the database'

    def handle(self, *args, **kwargs):
        # Sample courses data
        courses = [
            {
                'name': 'Mathematics 101',
                'questions': 10,
                'marks': 100
            },
            {
                'name': 'Physics Basics',
                'questions': 8,
                'marks': 80
            },
            {
                'name': 'Computer Science Fundamentals',
                'questions': 12,
                'marks': 120
            },
            {
                'name': 'English Literature',
                'questions': 15,
                'marks': 150
            }
        ]

        # Sample MCQ questions for Mathematics
        math_questions = [
            {
                'question': 'What is 2 + 2?',
                'options': ['3', '4', '5', '6'],
                'answer': '4',
                'marks': 10,
                'type': 'MCQ'
            },
            {
                'question': 'Solve for x: 2x = 10',
                'options': ['4', '5', '6', '7'],
                'answer': '5',
                'marks': 10,
                'type': 'MCQ'
            },
            {
                'question': 'What is the square root of 16?',
                'options': ['2', '3', '4', '5'],
                'answer': '4',
                'marks': 10,
                'type': 'MCQ'
            },
            {
                'question': 'Explain the concept of derivatives in calculus.',
                'model_answer': 'A derivative measures the rate of change of a function with respect to its variable.',
                'marks': 20,
                'type': 'ESSAY'
            }
        ]

        # Sample questions for Physics
        physics_questions = [
            {
                'question': "What is Newton's first law of motion?",
                'options': [
                    'Objects in motion stay in motion',
                    'Force equals mass times acceleration',
                    'An object at rest stays at rest unless acted upon by a force',
                    'Every action has an equal and opposite reaction'
                ],
                'answer': 'An object at rest stays at rest unless acted upon by a force',
                'marks': 10,
                'type': 'MCQ'
            },
            {
                'question': 'What is the SI unit of force?',
                'options': ['Newton', 'Joule', 'Watt', 'Pascal'],
                'answer': 'Newton',
                'marks': 10,
                'type': 'MCQ'
            },
            {
                'question': 'Explain the concept of gravity.',
                'model_answer': 'Gravity is a force of attraction between all objects with mass in the universe.',
                'marks': 20,
                'type': 'SHORT'
            }
        ]

        # Sample questions for Computer Science
        cs_questions = [
            {
                'question': 'What is an algorithm?',
                'options': [
                    'A programming language',
                    'A step-by-step procedure to solve a problem',
                    'A type of computer',
                    'A database'
                ],
                'answer': 'A step-by-step procedure to solve a problem',
                'marks': 10,
                'type': 'MCQ'
            },
            {
                'question': 'What does CPU stand for?',
                'options': [
                    'Central Processing Unit',
                    'Computer Personal Unit',
                    'Central Program Utility',
                    'Computer Processing Unit'
                ],
                'answer': 'Central Processing Unit',
                'marks': 10,
                'type': 'MCQ'
            },
            {
                'question': 'Explain the concept of object-oriented programming.',
                'model_answer': 'Object-oriented programming is a programming paradigm based on objects containing data and code.',
                'marks': 20,
                'type': 'ESSAY'
            }
        ]

        # Sample questions for English Literature
        english_questions = [
            {
                'question': 'Who wrote "Romeo and Juliet"?',
                'options': [
                    'William Shakespeare',
                    'Charles Dickens',
                    'Jane Austen',
                    'Mark Twain'
                ],
                'answer': 'William Shakespeare',
                'marks': 10,
                'type': 'MCQ'
            },
            {
                'question': 'What is a metaphor?',
                'options': [
                    'Direct comparison',
                    'Indirect comparison',
                    'Repetition of sounds',
                    'Question in poetry'
                ],
                'answer': 'Indirect comparison',
                'marks': 10,
                'type': 'MCQ'
            },
            {
                'question': 'Analyze the themes in "To Kill a Mockingbird".',
                'model_answer': 'The novel explores themes of racial injustice, moral growth, and the loss of innocence in the American South.',
                'marks': 30,
                'type': 'ESSAY'
            }
        ]

        course_questions = {
            'Mathematics 101': math_questions,
            'Physics Basics': physics_questions,
            'Computer Science Fundamentals': cs_questions,
            'English Literature': english_questions
        }

        # Create courses and questions
        for course_data in courses:
            course = Course.objects.create(
                course_name=course_data['name'],
                question_number=course_data['questions'],
                total_marks=course_data['marks']
            )
            
            # Add questions for this course
            questions = course_questions[course_data['name']]
            for q_data in questions:
                question = Question.objects.create(
                    course=course,
                    marks=q_data['marks'],
                    question=q_data['question'],
                    question_type=q_data['type']
                )
                
                if q_data['type'] == 'MCQ':
                    question.option1 = q_data['options'][0]
                    question.option2 = q_data['options'][1]
                    question.option3 = q_data['options'][2]
                    question.option4 = q_data['options'][3]
                    question.mcq_answer = q_data['answer']
                else:
                    question.model_answer = q_data['model_answer']
                
                question.save()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created course "{course_data["name"]}" with {len(questions)} questions')
            )
