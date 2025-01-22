from django.db import models
from student.models import Student


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()

    def __str__(self):
        return self.course_name


class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('ESSAY', 'Essay'),
        ('SHORT', 'Short Answer')
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    question_type = models.CharField(max_length=5, choices=QUESTION_TYPES, default='MCQ')

    # Fields for MCQ
    option1 = models.CharField(max_length=200, blank=True, null=True)
    option2 = models.CharField(max_length=200, blank=True, null=True)
    option3 = models.CharField(max_length=200, blank=True, null=True)
    option4 = models.CharField(max_length=200, blank=True, null=True)
    mcq_answer = models.CharField(max_length=200, blank=True, null=True)

    # Field for Essay/Short Answer model answers
    model_answer = models.TextField(blank=True, null=True, help_text="Model answer for essay or short answer questions")

    def __str__(self):
        return f"{self.question[:50]}... ({self.get_question_type_display()})"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    marks_obtained = models.PositiveIntegerField()
    answer_text = models.TextField(blank=True, null=True)  # For storing essay/short answer responses
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'exam', 'question']