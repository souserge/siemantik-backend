from rest_framework import serializers

from django.contrib.auth.models import User
from siemantik.app.models import Project, Label, Document, ClassifierModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'project_set')


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'classname', 'display_name')


class ProjectSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'user', 'name', 'language', 'description', 'labels')


class DocumentSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'label', 'is_set_manually')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'text', 'label', 'is_set_manually')

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'language', 'description')
    

class ProjectDocumentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=1000, allow_null=True)
    text = serializers.CharField()
    label_id = serializers.IntegerField(allow_null=True)


class ProjectLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('classname', 'display_name')


class ImportDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('title', 'text')

class ClassifierModelSerializer(serializers.ModelSerializer):
    cv_accuracy = serializers.SerializerMethodField()

    class Meta:
        model = ClassifierModel
        fields = ('id', 'name', 'used_algorithm', 'model_status', 'cv_accuracy')

    def get_cv_accuracy(self, obj):
        vr = obj.validation_results
        if vr is not None:
            return vr.get('accuracy')
        else:
            return None