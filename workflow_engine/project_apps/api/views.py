from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project_apps.api.serializers import serialize_workflow
from project_apps.service.workflow_service import WorkflowService

class WorkflowCreateAPIView(APIView):
    '''
    API View for creating a new Workflow instance along with associated Job instances.
    '''
    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        jobs_data = request.data.get('jobs', [])

        if not name or not description:
            return Response({'error': 'name and description are required.'}, status=status.HTTP_400_BAD_REQUEST)

        workflow_service = WorkflowService()
        try:
            workflow = workflow_service.create_workflow(name, description, jobs_data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(workflow, status=status.HTTP_201_CREATED)
