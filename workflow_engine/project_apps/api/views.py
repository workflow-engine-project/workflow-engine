from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project_apps.service.workflow_service import WorkflowService, WorkflowExecutor


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


class WorkflowReadAPIView(APIView):
    '''
    API View for reading the corresponding workflow record.
    '''
    def get(self, request, workflow_uuid):
        if not workflow_uuid:
            return Response({'error': 'workflow uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        workflow_service = WorkflowService()
        try:
            workflow = workflow_service.get_workflow(workflow_uuid)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(workflow, status=status.HTTP_200_OK)


class WorkflowUpdateAPIView(APIView):
    '''
    API View for updating the corresponding workflow record.
    '''
    def patch(self, request, workflow_uuid):
        workflow_data = request.data.dict()
        jobs_data = workflow_data.pop('jobs')

        if not workflow_uuid:
            return Response({'error': 'workflow uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        workflow_service = WorkflowService()
        try:
            workflow = workflow_service.update_workflow(workflow_uuid, workflow_data, jobs_data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(workflow, status=status.HTTP_200_OK)


class WorkflowDeleteAPIView(APIView):
    '''
    API View for deleting a Workflow instance along with associated Job instances.
    '''

    def delete(self, request, workflow_uuid):
        workflow_service = WorkflowService()

        try:
            # Workflow 및 해당 Workflow에 종속된 Jobs를 삭제
            workflow_service.delete_workflow(workflow_uuid)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': f'Workflow with uuid {workflow_uuid} and associated jobs deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)


class WorkflowListReadAPIView(APIView):
    '''
    API View for reading the whole workflow list.
    '''
    def get(self, request):
        workflow_service = WorkflowService()
        workflow_list = workflow_service.get_workflow_list()
        
        return Response(workflow_list, status=status.HTTP_200_OK)


class WorkflowExecuteAPIView(APIView):
    def get(self, request, workflow_uuid):
        '''
        Fetch the list of jobs to execute, belonging to the corresponding workflow uuid and cache it into Redis storage.

        Request data
        - uuid: workflow's uuid that you want to execute.
        '''
        workflow_executor = WorkflowExecutor()
        result = workflow_executor.execute_workflow(workflow_uuid)

        if result:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
