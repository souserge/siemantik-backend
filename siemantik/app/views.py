from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

from siemantik.app.models import Project, Label, Document
from siemantik.app.serializers import ProjectSerializer, LabelSerializer, ProjectDocumentSerializer,  ProjectLabelSerializer, DocumentSetSerializer, DocumentSerializer, CreateProjectSerializer


def get_user():
    return User.objects.get(id=1)


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


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
            )
            return Response(ProjectSerializer(project).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def labels(self, request, pk=None):
        project = self.get_object()
        if request.method == 'POST':
            serializer = ProjectLabelSerializer(data=request.data)
            if serializer.is_valid():
                label = serializer.save(project=project)
                return Response(LabelSerializer(label).data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(request.method + ' method not supported', status=status.HTTP_400_BAD_REQUEST)
        

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
