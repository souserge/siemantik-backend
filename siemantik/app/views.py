from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

from siemantik.app.models import Project, Label, Document, ClassifierModel, TRAINED, TRAINING
from siemantik.app.serializers import  LabelSerializer, ProjectLabelSerializer
from siemantik.app.serializers import ProjectSerializer, CreateProjectSerializer
from siemantik.app.serializers import DocumentSetSerializer, DocumentSerializer
from siemantik.app.serializers import ProjectDocumentSerializer, ImportDocumentSerializer
from siemantik.app.serializers import ClassifierModelSerializer

from siemantik.app.classifiers.classify import classify
from siemantik.app.classifiers.train import train 

def get_user():
    return User.objects.get(id=1)


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class ClassifierModelViewSet(viewsets.ModelViewSet):
    queryset = ClassifierModel.objects.all()
    serializer_class = ClassifierModelSerializer


    @action(detail=True, methods=['post'])
    def train(self, request, pk=None):
        model = self.get_object()
        model.model_status = TRAINING
        model.save()

        document_ids = request.data['documents']
        documents = map(lambda d: Document.objects.get(id=d), document_ids)

        estimator, validation_results = train(model.used_algorithm, documents)

        model.model_status = TRAINED
        model.estimator = estimator
        model.validation_results = validation_results
        model.save()

        return Response({ 'cv_accuracy': ClassifierModelSerializer.get_cv_accuracy(None, model) })


    @action(detail=True, methods=['post'])
    def classify(self, request, pk=None):
        document_ids = request.data['documents']
        documents = list(map(lambda d: Document.objects.get(id=d), document_ids))

        model = self.get_object()
        model.model_status = TRAINED
        model.save()
        print(documents)
        probabilities = classify(model.estimator, documents)
        print(probabilities)
        return Response(probabilities)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        serializer = CreateProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = Project.objects.create(
                user=get_user(),
                name=serializer.data['name'],
                language=serializer.data['language'],
                description=serializer.data['description']
            )
            return Response(ProjectSerializer(project).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def import_documents(self, request, pk=None):
        project = self.get_object()
        label_id = request.data['label']
        serializer = ImportDocumentSerializer(data=request.data['documents'], many=True)
        if serializer.is_valid():
            label = None
            is_set_manually = False
            if label_id is not None:
                label = Label.objects.get(id=label_id) 
                is_set_manually = True
            
            docs = serializer.save(project=project, label=label, is_set_manually=is_set_manually)
            return Response(DocumentSetSerializer(docs, many=True).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_doc_labels(self, request, pk=None):
        project = self.get_object()
        documents = request.data['documents']
        labels = Label.objects.all()
        for doc in documents:
            doc_model = Document.objects.get(id=doc.get('id'))
            doc_model.label = labels.get(id=doc.get('label'))
            doc_model.is_set_manually = False
            doc_model.save()
            print(doc_model)

        return Response('ok')




    @action(detail=True, methods=['post'])
    def labels(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectLabelSerializer(data=request.data)
        if serializer.is_valid():
            label = serializer.save(project=project)
            return Response(LabelSerializer(label).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True, methods=['get', 'post'])
    def documents(self, request, pk=None):
        project = self.get_object()
        if request.method == 'GET':
            serializer = DocumentSetSerializer(project.documents, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = ProjectDocumentSerializer(data=request.data)
            if serializer.is_valid():
                label = None
                is_set_manually = False
                if serializer.data.get('label_id') is not None:
                    label = project.labels.get(id=serializer.data['label_id'])
                    is_set_manually = True

                title = serializer.data.get('title')
                if title is None:
                    title = ''
                doc = Document.objects.create(
                    title=title,
                    text=serializer.data['text'],
                    label=label, 
                    is_set_manually=is_set_manually, 
                    project=project  
                )
                if serializer.data.get('title') is None:
                    doc.title = 'doc-' + str(doc.id)
                doc.save()
                return Response(DocumentSerializer(doc).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'])
    def models(self, request, pk=None):
        project = self.get_object()
        if request.method == 'GET':
            serializer = ClassifierModelSerializer(project.models, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = ClassifierModelSerializer(data=request.data)
            if serializer.is_valid():
                classifier_model = serializer.save(project=project)
                return Response(ClassifierModelSerializer(classifier_model).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

