from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project_apps.service.workflow_service import WorkflowService
from project_apps.service.scheduling_service import SchedulingService


class WorkflowAPIView(APIView):
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

    '''
    API View for updating the corresponding workflow record.
    '''
    def patch(self, request, workflow_uuid):
        workflow_data = request.data
        jobs_data = workflow_data.get('jobs', {})

        if not workflow_uuid:
            return Response({'error': 'workflow uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        workflow_service = WorkflowService()
        try:
            workflow = workflow_service.update_workflow(workflow_uuid, workflow_data, jobs_data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(workflow, status=status.HTTP_200_OK)

    '''
    API View for deleting a Workflow instance along with associated Job instances.
    '''

    def delete(self, request, workflow_uuid):
        workflow_service = WorkflowService()

        try:
            # Workflow 및 해당 Workflow에 종속된 Jobs를 삭제
            result = workflow_service.delete_workflow(workflow_uuid)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if result:
            return Response({'success': f'Workflow with uuid {workflow_uuid} and associated jobs deleted successfully.'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'fail': f'Workflow with uuid {workflow_uuid} and associated jobs does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)


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
        workflow_service = WorkflowService()
        result = workflow_service.execute_workflow(workflow_uuid)

        if result:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SchedulingAPIView(APIView):
    '''
    API View for creating a new Scheduling instance.
    '''
    def post(self, request):
        workflow_uuid = request.data.get('workflow_uuid')
        scheduled_at = request.data.get('scheduled_at')
        interval = request.data.get('interval')
        repeat_count = request.data.get('repeat_count', 0)

        if not workflow_uuid:
            return Response({'error': 'workflow_uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        scheduling_service = SchedulingService()
        try:
            scheduling = scheduling_service.create_scheduling(workflow_uuid, scheduled_at, interval, repeat_count)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(scheduling, status=status.HTTP_201_CREATED)

    '''
    API View for reading the corresponding scheduling record.
    '''
    def get(self, request, scheduling_uuid):
        if not scheduling_uuid:
            return Response({'error': 'scheduling uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        scheduling_service = SchedulingService()
        try:
            scheduling = scheduling_service.get_scheduling(scheduling_uuid)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(scheduling, status=status.HTTP_200_OK)

    '''
    API View for updating the corresponding scheduling record.
    '''
    def patch(self, request, scheduling_uuid):
        scheduling_data = request.data

        if not scheduling_uuid:
            return Response({'error': 'scheduling uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        scheduling_service = SchedulingService()
        try:
            scheduling = scheduling_service.update_scheduling(scheduling_uuid, scheduling_data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(scheduling, status=status.HTTP_200_OK)

    '''
    API View for deleting a scheduling instance.
    '''
    def delete(self, request, scheduling_uuid):
        scheduling_service = SchedulingService()

        try:
            scheduling_service.delete_scheduling(scheduling_uuid)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': f'Scheduling with uuid {scheduling_uuid} deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)


class SchedulingListReadAPIView(APIView):
    '''
    API View for reading the whole scheduling list.
    '''
    def get(self, request, workflow_uuid):
        scheduling_service = SchedulingService()
        scheduling_list = scheduling_service.get_scheduling_list(workflow_uuid)

        return Response(scheduling_list, status=status.HTTP_200_OK)


class SchedulingExecuteAPIView(APIView):
    '''
    API View for execute scheduling. 
    '''
    def post(self, request, scheduling_uuid):
        scheduling_service = SchedulingService()
        success, message = scheduling_service.activate_scheduling(scheduling_uuid)

        if not success:
            return Response({"error": message}, status=400)

        return Response({"message": message})
