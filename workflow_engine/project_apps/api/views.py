from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project_apps.service.workflow_service import WorkflowService
from project_apps.service.scheduling_service import SchedulingService


class WorkflowAPIView(APIView):
    '''
    Workflow를 생성하거나 모든 Workflow의 정보와 
    각각의 Job 리스트를 반환하는 API.
    '''
    @swagger_auto_schema(
    operation_summary="워크플로우 생성",
    operation_description="워크플로우 및 관련 작업(Job)들을 생성합니다.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'description', 'jobs'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='워크플로우 이름'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='워크플로우 내용'),
            'jobs': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description='Job 목록',
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    required=['name', 'image'],
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Job 이름'),
                        'image': openapi.Schema(type=openapi.TYPE_STRING, description='실행할 컨테이너 이미지'),
                        'parameters': openapi.Schema(
                            type=openapi.TYPE_OBJECT, 
                            description='Job 실행에 필요한 파라미터', 
                            additional_properties=True, 
                            default={}
                        ),
                        'next_job_names': openapi.Schema(
                            type=openapi.TYPE_ARRAY, 
                            description='이 Job이 완료된 후 실행될 Job의 이름 목록', 
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            default=[]
                        ),
                        'timeout': openapi.Schema(
                            type=openapi.TYPE_INTEGER, 
                            description='Job의 최대 실행 시간(초)', 
                            default=0
                        ),
                        'retries': openapi.Schema(
                            type=openapi.TYPE_INTEGER, 
                            description='Job 실패 시 재시도 횟수', 
                            default=0
                        ),
                    },
                ),
            ),
        },
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(description='워크플로우 생성 성공'),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description='잘못된 요청 데이터'),
        }
    )
    def post(self, request):
        '''
        입력 받은 데이터를 바탕으로 Workflow와 Job 리스트를 생성한다.
        '''
        name = request.data.get('name')
        description = request.data.get('description')
        jobs_data = request.data.get('jobs', [])

        if not name or not description:
            return Response({'error': 'name and description are required.'}, status=status.HTTP_400_BAD_REQUEST)

        workflow_service = WorkflowService()
        try:
            workflow = workflow_service.create_workflow(name, description, jobs_data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(workflow, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
    operation_summary="전체 워크플로우 조회",
    operation_description="모든 워크플로우와 각각의 Job 리스트를 반환합니다.",
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="모든 워크플로우 리스트 반환 성공",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='워크플로우 UUID'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='워크플로우 이름'),
                        'description': openapi.Schema(type=openapi.TYPE_STRING, description='워크플로우 설명'),
                        'jobs': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            description='워크플로우에 속한 Job 목록',
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Job 이름'),
                                    'image': openapi.Schema(type=openapi.TYPE_STRING, description='실행할 컨테이너 이미지'),
                                    'parameters': openapi.Schema(
                                        type=openapi.TYPE_OBJECT, 
                                        description='Job 실행에 필요한 파라미터', 
                                        additional_properties=True
                                    ),
                                    'next_job_names': openapi.Schema(
                                        type=openapi.TYPE_ARRAY, 
                                        description='다음에 실행될 Job 이름 목록',
                                        items=openapi.Items(type=openapi.TYPE_STRING)
                                    ),
                                    'timeout': openapi.Schema(
                                        type=openapi.TYPE_INTEGER, 
                                        description='Job의 최대 실행 시간(초)'
                                    ),
                                    'retries': openapi.Schema(
                                        type=openapi.TYPE_INTEGER, 
                                        description='Job 실패 시 재시도 횟수'
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            )
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="잘못된 요청")
        }
    )
    def get(self, request):
        '''
        모든 Workflow의 리스트를 반환한다.
        '''
        workflow_service = WorkflowService()
        workflow_list = workflow_service.get_workflow_list()
        
        return Response(workflow_list, status=status.HTTP_200_OK)


class WorkflowUUIDAPIView(APIView):
    '''
    Workflow 정보를 관리하는 API.
    '''
    @swagger_auto_schema(
        operation_summary="특정 워크플로우 조회",
        operation_description="입력 받은 UUID에 해당하는 워크플로우와 그에 포함된 Job 리스트를 반환합니다.",
        manual_parameters=[
            openapi.Parameter(
                name='workflow_uuid',
                in_=openapi.IN_PATH,
                description="조회하고자 하는 워크플로우의 UUID",
                required=True,
                type=openapi.TYPE_STRING,
                format='uuid'
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="워크플로우 조회 성공",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='워크플로우 이름'),
                        'description': openapi.Schema(type=openapi.TYPE_STRING, description='워크플로우 설명'),
                        'jobs': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            description='워크플로우에 포함된 Job 목록',
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Job UUID'),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Job 이름'),
                                    'image': openapi.Schema(type=openapi.TYPE_STRING, description='실행 이미지'),
                                    'parameters': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description='Job 실행 파라미터',
                                        additional_properties=True
                                    ),
                                    'next_job_names': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Items(type=openapi.TYPE_STRING),
                                        description='다음에 실행될 Job 이름 목록'
                                    ),
                                    'timeout': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='최대 실행 시간(초)'
                                    ),
                                    'retries': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='실패 시 재시도 횟수'
                                    ),
                                }
                            )
                        ),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="잘못된 요청"),
            status.HTTP_404_NOT_FOUND: openapi.Response(description="워크플로우를 찾을 수 없음")
        }
    )
    def get(self, request, workflow_uuid):
        '''
        입력 받은 Workflow와 그에 포함된 Job 리스트를 반환한다.
        '''
        if not workflow_uuid:
            return Response({'error': 'workflow uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        workflow_service = WorkflowService()
        try:
            workflow = workflow_service.get_workflow(workflow_uuid)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(workflow, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="특정 워크플로우 수정",
        operation_description="입력 받은 Workflow와 Job 리스트를 주어진 데이터로 수정합니다.",
        manual_parameters=[
            openapi.Parameter(
                name='workflow_uuid',
                in_=openapi.IN_PATH,
                description="수정하고자 하는 워크플로우의 UUID",
                required=True,
                type=openapi.TYPE_STRING,
                format='uuid'
            )
        ],
        request_body=openapi.Schema(  # 요청 본문의 스키마 정의
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='워크플로우의 새 이름'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='워크플로우의 새 설명'),
                'jobs': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description='업데이트할 작업(Job)들의 목록',
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        required=['uuid'],
                        properties={
                            'uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='작업의 UUID'),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='작업의 새 이름'),
                            'image': openapi.Schema(type=openapi.TYPE_STRING, description='작업의 새 이미지'),
                            'parameters': openapi.Schema(
                                type=openapi.TYPE_OBJECT, 
                                description='작업의 새 파라미터'
                            ),
                            'next_job_names': openapi.Schema(
                                type=openapi.TYPE_ARRAY, 
                                description='작업이 완료된 후 실행될 다음 작업들의 이름 목록',
                                items=openapi.Items(type=openapi.TYPE_STRING),
                            ),
                            'timeout': openapi.Schema(type=openapi.TYPE_INTEGER, description='작업의 새 최대 실행 시간(초)'),
                            'retries': openapi.Schema(type=openapi.TYPE_INTEGER, description='작업의 새 실패 시 재시도 횟수'),
                        },
                    ),
                ),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(description='워크플로우 업데이트 성공'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='잘못된 요청 데이터'),
        }
    )
    def patch(self, request, workflow_uuid):
        '''
        입력 받은 Workflow와 Job 리스트를 주어진 데이터로 수정한다.
        '''
        workflow_data = request.data
        jobs_data = workflow_data.get('jobs', {})

        if not workflow_uuid:
            return Response({'error': 'workflow uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        workflow_service = WorkflowService()
        try:
            workflow = workflow_service.update_workflow(workflow_uuid, workflow_data, jobs_data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(workflow, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="특정 워크플로우 삭제",
        operation_description="입력 받은 UUID에 해당하는 워크플로우와 그에 포함된 모든 Job 리스트를 삭제합니다.",
        manual_parameters=[
            openapi.Parameter(
                name='workflow_uuid',
                in_=openapi.IN_PATH,
                description="삭제하고자 하는 워크플로우의 UUID",
                required=True,
                type=openapi.TYPE_STRING,
                format='uuid'
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="워크플로우 및 연관된 Job 리스트 삭제 성공"
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="잘못된 요청 또는 UUID 형식 오류"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="지정된 UUID를 가진 워크플로우를 찾을 수 없음"
            ),
        }
    )
    def delete(self, request, workflow_uuid):
        '''
        입력 받은 Workflow와 Job 리스트를 삭제한다.
        '''
        workflow_service = WorkflowService()

        try:
            result = workflow_service.delete_workflow(workflow_uuid)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if result:
            return Response({'success': f'Workflow with uuid {workflow_uuid} and associated jobs deleted successfully.'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'fail': f'Workflow with uuid {workflow_uuid} and associated jobs does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)


class WorkflowExecuteAPIView(APIView):
    '''
    Workflow를 실행하는 API.
    '''
    @swagger_auto_schema(
        operation_summary="특정 워크플로우 실행",
        operation_description="입력 받은 UUID에 해당하는 워크플로우를 실행합니다.",
        manual_parameters=[
            openapi.Parameter(
                name='workflow_uuid',
                in_=openapi.IN_PATH,
                description="실행하고자 하는 워크플로우의 UUID",
                required=True,
                type=openapi.TYPE_STRING,
                format='uuid'
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="워크플로우 실행 성공"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="지정된 UUID를 가진 워크플로우를 찾을 수 없음"
            )
        }
    )
    def get(self, request, workflow_uuid):
        '''
        입력 받은 Workflow를 수행한다.
        '''
        workflow_service = WorkflowService()
        result = workflow_service.execute_workflow(workflow_uuid)

        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SchedulingAPIView(APIView):
    '''
    Scheduling을 생성하거나 모든 Scheduling 정보를 반환하는 API.
    '''
    @swagger_auto_schema(
        operation_summary="스케줄링 생성",
        operation_description="입력 받은 데이터를 바탕으로 Scheduling을 생성합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['workflow_uuid'],
            properties={
                'workflow_uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Workflow의 UUID'),
                'scheduled_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='스케줄링 시작 시각 (옵션)'),
                'interval': openapi.Schema(type=openapi.TYPE_OBJECT, description='실행 간격 (옵션)',                                           properties={
                                               'hours': openapi.Schema(type=openapi.TYPE_INTEGER, description='시간'),
                                               'minutes': openapi.Schema(type=openapi.TYPE_INTEGER, description='분'),
                                               'seconds': openapi.Schema(type=openapi.TYPE_INTEGER, description='초')
                                           }),
                'repeat_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='반복 횟수 (기본값: 0)'),
            },
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(description='스케줄링 생성 성공'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='잘못된 요청 데이터'),
        }
    )
    def post(self, request):
        '''
        입력 받은 데이터를 바탕으로 Scheduling을 생성한다.
        '''
        workflow_uuid = request.data.get('workflow_uuid')
        scheduled_at = request.data.get('scheduled_at')
        interval = request.data.get('interval')
        repeat_count = request.data.get('repeat_count', 0)

        if not workflow_uuid:
            return Response({'error': 'workflow_uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        scheduling_service = SchedulingService()
        try:
            scheduling = scheduling_service.create_scheduling(workflow_uuid, scheduled_at, interval, repeat_count)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(scheduling, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="모든 스케줄링 정보 조회",
        operation_description="저장된 모든 스케줄링 정보의 리스트를 반환합니다.",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="모든 스케줄링 정보 조회 성공",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='스케줄링 UUID'),
                            'workflow_uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Workflow의 UUID'),
                            'scheduled_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='스케줄링 시작 시각'),
                            'interval': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description='실행 간격',
                                properties={
                                    'hours': openapi.Schema(type=openapi.TYPE_INTEGER, description='시간'),
                                    'minutes': openapi.Schema(type=openapi.TYPE_INTEGER, description='분'),
                                    'seconds': openapi.Schema(type=openapi.TYPE_INTEGER, description='초'),
                                }
                            ),
                            'repeat_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='반복 횟수'),
                        }
                    )
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='잘못된 요청')
        }
    )
    def get(self, request):
        '''
        모든 Scheduling의 리스트를 반환한다.
        '''
        scheduling_service = SchedulingService()
        scheduling_list = scheduling_service.get_scheduling_list()

        return Response(scheduling_list, status=status.HTTP_200_OK)


class SchedulingUUIDAPIView(APIView):
    '''
    Scheduling 정보를 관리하는 API.
    '''
    @swagger_auto_schema(
    operation_summary="특정 스케줄링 정보 조회",
    operation_description="UUID를 통해 특정 스케줄링 정보를 조회합니다.",
    manual_parameters=[
        openapi.Parameter(
            name='scheduling_uuid',
            in_=openapi.IN_PATH,
            description="조회하고자 하는 스케줄링의 UUID",
            required=True,
            type=openapi.TYPE_STRING,
            format='uuid'
        )
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="스케줄링 정보 조회 성공",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='스케줄링 UUID'),
                    'workflow_uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='연관된 Workflow의 UUID'),
                    'scheduled_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='스케줄링 시작 시각'),
                    'interval': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description='실행 간격',
                        properties={
                            'hours': openapi.Schema(type=openapi.TYPE_INTEGER, description='시간'),
                            'minutes': openapi.Schema(type=openapi.TYPE_INTEGER, description='분'),
                            'seconds': openapi.Schema(type=openapi.TYPE_INTEGER, description='초')
                        }
                    ),
                    'repeat_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='반복 횟수'),
                }
            )
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="잘못된 요청")
        }
    )
    def get(self, request, scheduling_uuid):
        '''
        입력 받은 Scheduling을 반환한다.
        '''
        if not scheduling_uuid:
            return Response({'error': 'scheduling uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        scheduling_service = SchedulingService()
        try:
            scheduling = scheduling_service.get_scheduling(scheduling_uuid)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(scheduling, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="특정 스케줄링 데이터 수정",
        operation_description="특정 Scheduling을 전송 받은 데이터로 수정합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'scheduled_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='스케줄링 시작 시각'),
                'interval': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='실행 간격 (옵션)',
                    properties={
                        'hours': openapi.Schema(type=openapi.TYPE_INTEGER, description='시간'),
                        'minutes': openapi.Schema(type=openapi.TYPE_INTEGER, description='분'),
                        'seconds': openapi.Schema(type=openapi.TYPE_INTEGER, description='초')
                    }
                ),
                'repeat_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='반복 횟수'),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(description='스케줄링 업데이트 성공'),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description='잘못된 요청 데이터'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='해당 UUID를 가진 스케줄링을 찾을 수 없음'),
        }
    )
    def patch(self, request, scheduling_uuid):
        '''
        Scheduling을 전송 받은 데이터로 수정한다.
        '''
        scheduling_data = request.data

        if not scheduling_uuid:
            return Response({'error': 'scheduling uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

        scheduling_service = SchedulingService()
        try:
            success, result = scheduling_service.update_scheduling(scheduling_uuid, scheduling_data)
            if success:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response({"error": result}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="특정 스케줄링 삭제",
        operation_description="특정 Scheduling을 삭제합니다.",
        manual_parameters=[
            openapi.Parameter(
                name='scheduling_uuid',
                in_=openapi.IN_PATH,
                description="삭제하고자 하는 스케줄링의 UUID",
                required=True,
                type=openapi.TYPE_STRING,
                format='uuid'
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description="스케줄링 삭제 성공. 반환되는 본문 없음."),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="잘못된 요청. 예를 들어, 유효하지 않은 UUID 형식 등.")
        }
    )
    def delete(self, request, scheduling_uuid):
        '''
        입력 받은 Scheduling을 삭제한다.
        '''
        scheduling_service = SchedulingService()

        try:
            scheduling_service.delete_scheduling(scheduling_uuid)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': f'Scheduling with uuid {scheduling_uuid} deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)


class SchedulingWorkflowAPIView(APIView):
    '''
    특정 워크플로우에 종속된 Scheduling의 정보와 각각의 Job 리스트를 반환하는 API.
    '''
    @swagger_auto_schema(
        operation_summary="특정 워크플로우에 종속된 스케줄링 정보 조회",
        operation_description="입력 받은 워크플로우 UUID에 종속된 모든 스케줄링의 정보와 각 스케줄링에 속한 Job 리스트를 반환합니다.",
        manual_parameters=[
            openapi.Parameter(
                name='workflow_uuid',
                in_=openapi.IN_PATH,
                description="조회하고자 하는 워크플로우의 UUID",
                required=True,
                type=openapi.TYPE_STRING,
                format='uuid'
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="워크플로우에 종속된 스케줄링 정보 조회 성공",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='스케줄링 UUID'),
                            'workflow_uuid': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='연관된 워크플로우의 UUID'),
                            'scheduled_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='스케줄링 시작 시각'),
                            'interval': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description='실행 간격',
                                properties={
                                    'hours': openapi.Schema(type=openapi.TYPE_INTEGER, description='시간'),
                                    'minutes': openapi.Schema(type=openapi.TYPE_INTEGER, description='분'),
                                    'seconds': openapi.Schema(type=openapi.TYPE_INTEGER, description='초'),
                                }
                            ),
                            'repeat_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='반복 횟수'),
                        }
                    )
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="잘못된 요청")
        }
    )
    def get(self, request, workflow_uuid):
        '''
        특정 워크플로우에 종속된 Scheduling의 리스트를 반환한다.
        '''
        scheduling_service = SchedulingService()
        scheduling_list = scheduling_service.get_workflow_scheduling_list(workflow_uuid)

        return Response(scheduling_list, status=status.HTTP_200_OK)


class SchedulingExecuteAPIView(APIView):
    '''
    Scheduling을 활성화하는 API.
    '''
    @swagger_auto_schema(
    operation_summary="스케줄링 활성화",
    operation_description="입력 받은 UUID에 해당하는 스케줄링을 활성화합니다.",
    manual_parameters=[
        openapi.Parameter(
            name='scheduling_uuid',
            in_=openapi.IN_PATH,
            description="활성화하고자 하는 스케줄링의 UUID",
            required=True,
            type=openapi.TYPE_STRING,
            format='uuid'
        )
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="스케줄링 활성화 성공"
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="잘못된 요청 또는 활성화 실패")
        }
    )
    def post(self, request, scheduling_uuid):
        '''
        입력 받은 Scheduling을 활성화한다.
        '''
        scheduling_service = SchedulingService()
        success, message = scheduling_service.activate_scheduling(scheduling_uuid)

        if not success:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": message}, status=status.HTTP_200_OK)


class SchedulingDeactivateAPIView(APIView):
    '''
    Scheduling을 비활성화하는 API.
    '''
    @swagger_auto_schema(
    operation_summary="스케줄링 비활성화",
    operation_description="입력 받은 UUID에 해당하는 스케줄링을 비활성화합니다.",
    manual_parameters=[
        openapi.Parameter(
            name='scheduling_uuid',
            in_=openapi.IN_PATH,
            description="비활성화하고자 하는 스케줄링의 UUID",
            required=True,
            type=openapi.TYPE_STRING,
            format='uuid'
        )
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="스케줄링 비활성화 성공"
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="잘못된 요청 또는 비활성화 실패")
        }
    )
    def post(self, request, scheduling_uuid):
        '''
        입력 받은 Scheduling을 비활성화한다.
        '''
        scheduling_service = SchedulingService()
        success, message = scheduling_service.deactivate_scheduling(scheduling_uuid)

        if not success:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": message}, status=status.HTTP_200_OK)
