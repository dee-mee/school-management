from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name','question_number','total_marks']

class QuestionForm(forms.ModelForm):
    courseID = forms.ModelChoiceField(queryset=models.Course.objects.all(),
                                      empty_label="Course Name",
                                      to_field_name="id")

    class Meta:
        model = models.Question
        fields = ['marks', 'question', 'question_type', 'option1', 'option2',
                  'option3', 'option4', 'mcq_answer', 'model_answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'model_answer': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make MCQ fields not required initially
        mcq_fields = ['option1', 'option2', 'option3', 'option4', 'mcq_answer']
        for field in mcq_fields:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')

        if question_type == 'MCQ':
            # Validate MCQ fields are filled for MCQ type
            mcq_fields = ['option1', 'option2', 'option3', 'option4', 'mcq_answer']
            for field in mcq_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for MCQ questions')
        else:
            # Validate model answer is provided for essay/short answer
            if not cleaned_data.get('model_answer'):
                self.add_error('model_answer',
                               'Model answer is required for essay/short answer questions')

        return cleaned_data