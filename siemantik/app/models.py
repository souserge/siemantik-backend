import uuid
from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField

LANGUAGE_CHOICES = [('ru', 'Russian')]

ALGORITHM_CHOICES = [
    ('nb', 'Naive Bayes'),
    ('svm', 'Support Vector Machine'),
    ('mlp', 'Multi Layer Perceprton'),
]

NOT_TRAINED = 0
TRAINING = 1
TRAINED = 2

MODEL_STATUS_CHOICES = [
    (NOT_TRAINED, 'Not trained'),
    (TRAINING, 'Training'),
    (TRAINED, 'Trained')
]


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    language = models.CharField(
        max_length=3,
        choices=LANGUAGE_CHOICES,
        default=LANGUAGE_CHOICES[0],
        blank=False,
    )


class Label(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='labels')
    classname = models.CharField(max_length=100, blank=False)
    display_name = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ('classname', 'project')


class Document(models.Model):
    title = models.CharField(max_length=1000, blank=True)
    text = models.TextField()
    label = models.ForeignKey(Label, null=True, on_delete=models.SET_NULL)
    is_set_manually = models.BooleanField(default=False)
    label_probability = models.FloatField(blank=True, default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')



class ClassifierModel(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    used_algorithm = models.CharField(
        max_length=100,
        choices=ALGORITHM_CHOICES, 
        default=ALGORITHM_CHOICES[0],
        blank=False,
    )
    estimator = PickledObjectField()
    model_status = models.IntegerField(
        choices=MODEL_STATUS_CHOICES,
        default=NOT_TRAINED,
        blank=False
    )
    validation_results = PickledObjectField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='models')
