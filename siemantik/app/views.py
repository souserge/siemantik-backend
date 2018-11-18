from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

from siemantik.app.models import Project, Label, Document
from siemantik.app.serializers import ProjectSerializer, LabelSerializer, ProjectDocumentSerializer, DocumentSetSerializer, DocumentSerializer, CreateProjectSerializer


def get_user():
    return User.objects.get(id=1)


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
                print(serializer.data)
                if serializer.data.get('label_id') is not None:
                    label = project.labels.get(id=serializer.data['label_id'])
                    is_set_manually = True

                doc = Document.objects.create(
                    title=serializer.data['title'],
                    text=serializer.data['text'],
                    label=label, 
                    is_set_manually=is_set_manually, 
                    project=project  
                )
                doc.save()
                return Response(DocumentSerializer(doc).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
