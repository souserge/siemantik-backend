import uuid
from django.db import models
from django.contrib.auth.models import User


LANGUAGE_CHOICES = [('ru', 'Russian')]

ALGORITHM_CHOICES = [
    ('nb', 'Naive Bayes'),
    ('svm', 'Support Vector Machine'),
    ('mlp', 'Multi Layer Perceprton'),
]


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    language = models.CharField(
        max_length=3,
        choices=LANGUAGE_CHOICES,
        default=LANGUAGE_CHOICES[0],
        blank=False,
    )


class Label(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    classname = models.CharField(max_length=100, blank=True, unique=True)


class Document(models.Model):
    title = models.CharField(max_length=100, blank=True)
    text = models.TextField()
    label = models.ForeignKey(Label, null=True, on_delete=models.SET_NULL)
    is_set_manually = models.BooleanField(default=False)


class Classifier(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    used_algorithm = models.CharField(
        max_length=100,
        choices=ALGORITHM_CHOICES, 
        default=ALGORITHM_CHOICES[0],
        blank=False,
    )
    model_data = models.CharField(max_length=2500, blank=False)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
