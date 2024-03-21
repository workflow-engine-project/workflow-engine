# 워크플로우 엔진 프로젝트

## 프로젝트 소개
워크플로우 엔진 개발 프로젝트에 오신 것을 환영합니다! 이 프로젝트는 각 작업을 의존성으로 묶어서 순서대로 실행시키는 워크플로우를 구현하는 데 중점을 두고 있습니다. 또한 각 작업은 도커 이미지를 불러와서 도커 컨테이너를 실행시키는 작업을 수행합니다. 이 프로젝트는 스케줄링 기능을 제공하여 워크플로우를 예약 실행하고 주기성을 설정하여 반복 실행하는 기능도 지원합니다.

## 핵심 기능
- 워크플로우 정의: 각 작업을 정의하고 의존성으로 묶어 하나의 워크플로우로 정의한다.
- 워크플로우 실행: 구성한 워크플로우에 따라 각 작업을 순서대로 실행한다.
- 도커 컨테이너 실행: 각 작업은 도커 이미지를 불러와서 도커 컨테이너를 실행한다.
- 스케줄링 기능: 예약 실행 및 주기적인 반복 실행이 가능한 스케줄링 기능을 제공한다.

## 팀원 소개
<table>
  <tr>
    <td align="center" width="150px">
      <a href="https://github.com/giyong-choi" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/137133519?v=4" alt="최기용 프로필" />
      </a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/minsuhaha" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/105342203?v=4" alt="하민수 프로필" />
      </a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/hwan3526" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/41356191?v=4" alt="이지환 프로필" />
      </a>
    </td>
    <td align="center" width="150px">
      <a href="https://github.com/Ohhong" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/48611456?v=4" alt="오정재 프로필" />
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/giyong-choi" target="_blank">
        최기용
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/minsuhaha" target="_blank">
        하민수
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/hwan3526" target="_blank">
        이지환
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Ohhong" target="_blank">
        오정재(멘토)
      </a>
    </td>
  </tr>
</table>

## 개발 환경
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/4091ccd9-e339-4cb2-abbc-c47e508d0bb6)

## 팀 그라운드 룰 및 컨벤션
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/d2e2b0b3-3c0f-42a5-918e-4fe371d8aa8f)

### 업무 관리
업무 관리는 Jira를 사용했으며, 애자일 방법론 중 스크럼(스프린트) 방식으로 진행했습니다.
> 프로젝트를 완수하는데 시간이 제한적이고, 빠른시간 내에 프로젝트를 효율적으로 마무리하기 위해 애자일 방법론 중 스크럼 방식을 적용해 여러 스프린트 기간을 거쳤습니다.
- 리뷰 & 플래닝 : 2일(각 1일)
- 작업기간 : 2주
- 기간은 고정되어 있지 않으며 유동적이다.
- 스탠드 업 미팅 : 매일 오전 10시

### 문서 정리
문서 정리는 Notion을 사용했습니다.
> 사용자의 필요에 따라 자유롭게 페이지를 구성하고 커스터마이징할 수 있는 기능을 제공해 사용성이 좋고, 실시간으로 팀원들과 문서를 공유하고 편집할 수 있다는 점이 협업도구로써 유용하다고 판단하여 선택했습니다.

### 팀원 간 소통
Slack으로 진행하고자 했으나, 상호 간 피드백이 느리고 미팅 제한으로 인해 가장 익숙한 Discord로 변경했습니다.
> 메시지 기록, 채널 및 스레드를 통한 주제별 토론, 일회성 회의뿐만 아니라 프로젝트의 전체기간 동안 지속적인 커뮤니케이션이 가능해 선택했습니다.

### 버전 관리
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/578079a4-2c76-4793-8daf-630e6852aaff)

브랜치 전략은 GitHub Flow 전략을 적용했습니다.
> 해당 프로젝트가 기간이 정해진 소규모 프로젝트였기 때문에 빠른 생산속도를 위해서 기능별 브랜치를 생성하고 master 브랜치에 곧바로 merge 하는 GitHub Flow 전략을 사용했습니다. 

### 회의 시간
주기적으로 멘토링과 팀회의를 열었고, 이를 회의록으로 남겼습니다. 그리고 더 좋은 코드를 작성하기 위해 스터디를 개최했습니다.

![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/15006e74-7824-4896-bb40-d72a9e4aca2a)

#### 멘토링
- 월요일 오후 9시

#### 팀 회의
- 화요일 오전 10시
    - 멘토링 이후 정리 회의
- 월요일 오후 2시
    - 멘토링 발표 전 회의

#### 스터디
- 교재
    - 파이썬 코딩의 기술 개정2판 (Effective Python 2nd)
- 분량
    - 주당 1 챕터씩 진행
- 스터디 시간
    - 화요일 오전 11시
- 발표자 로테이션

## 프로젝트 일정
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/7ac1766f-5c61-4fa7-bc86-5141ffbd5375)

### 스프린트1 (2023/12/04~2023/12/11)
Jenkins 및 Airflow 의 기능을 사용하고, 어떤 기능을 개발할지 추출한다.
```
- Jenkins 및 Airflow 기능을 분석하고 문서로 작성한다.
- Jenkins 및 Airflow 예제를 실습한다.
- 워크플로우 엔진 개발을 위한 요구사항을 작성한다.
```

### 스프린트2 (2023/12/13~2023/12/18)
기능 요구사항을 확정하고, 설계를 시작한다.
```
- Docker 실습을 진행한다.
- 기능 요구사항을 확정한다.
```

### 스프린트3 (2023/12/19~2023/12/26)
설계 및 개발준비를 완료한다.
```
- 설계를 진행한다.
- 인프라스트럭처 설계도를 완성한다.
- 데이터베이스 모델을 확정한다.
- Celery를 공부한다.
- 리포지토리 패턴을 공부한다.
- 결정된 컴포넌트의 개발환경을 세팅한다.
```

### 스프린트4 (2023/12/27~2024/01/08)
설계를 마무리하고 코어 로직을 작성한다.
```
- 깃허브 리포지토리를 세팅한다.
- 장고 프로젝트를 세팅한다.
- 데이터베이스를 세팅한다.
- 리포지토리 패턴을 적용해 데이터베이스 레이어를 분리한다.
- Redis 클라이언트 코드를 작성한다.
- Celery worker를 띄우는 로직을 작업한다.
- 깃 디렉터리 리팩터링 작업을 진행한다.
```

### 스프린트5 (2024/01/09~2024/01/22)
워크플로우 실행 로직을 확정한다.
```
- 워크플로우 실행 로직을 정리한다.
```

### 스프린트6 (2024/01/23~2024/02/05)
워크플로우 CRUD와 실행 로직을 구현한다.
```
- 워크플로우 CRUD API를 개발한다.
- 워크플로우 실행 API를 구현한다.
- job을 수행하는 로직을 구현한다.
- job 의존성 관련 알고리즘을 구현한다.
```

### 스프린트7 (2024/02/06~2024/02/19)
MVP1 리팩터링을 진행한다.
```
- 객체 지향 5원칙(SOLID)에 관해 공부한다.
- 파이썬 GIL 및 분산 Lock 에 대해서 공부한다.
- Redis lock을 적용하는 로직을 구현한다.
- Docker 컨테이너의 환경변수 적용 로직을 구현한다.
- MVP1 리팩터링 전 발생했던 버그를 수정한다.
- 순환 import 문제를 해결한다.
- `HistoryRepository` 의 `update_history_status()` 메서드를 수정한다.
- `update_workflow()` 메서드에 `@transaction` 데코레이터를 추가한다.
- CRUD API 관련 리팩터링을 진행한다.
- 워크플로우 Read API의 에러를 수정한다.
- 워크플로우 Update API의 에러를 수정한다.
- 워크플로우 Delete API 요청 시에 발생하는 에러를 수정한다.
- 워크플로우 Delete API의 실패 시 처리 과정을 리팩터링한다.
- 워크플로우 CRUD API 뷰 클래스를 하나로 통합한다.
- 워크플로우 CRUD API의 serialize 과정을 리팩터링한다.
- 워크플로우의 수정된 데이터에 기반하여 depends_count가 변경되도록 로직을 수정한다.
- `Job` 테이블의 `parameters`, `next_job_names` 필드를 JSON으로 파싱한다.
- `Job` 테이블의 `next_job_names` 필드를 JSON으로 파싱하는 에러를 수정한다.
- job 실행 로직과 job 의존성 관련 로직을 분리한다.
- job의 timeout 및 retry 옵션 값 설정을 구현한다.
- job이 실패 처리되었을 경우 해당 워크플로우의 실행중인 job들도 모두 종료하는 로직으로 수정한다.
```

### 스프린트8 (2024/02/19~2024/03/04)
스케줄링 기능을 개발한다.
```
- 스케줄링 실행 로직을 확정 및 구현한다.
- 스케줄링 실행 API를 구현한다.
- 스케줄링 DB 모델을 확정 및 수정한다.
- 스케줄링 DB에서 `is_active` 필드의 default 옵션 값을 수정한다.
- 스케줄링 CRUD API를 구현한다.
- 스케줄링 Create 로직을 수정한다.
- 수정된 스케줄링 DB 관련 CRUD API 리팩터링 작업을 진행한다.
```

### 스프린트9,10 (2024/03/04~2024/03/15)
MVP2 리팩터링을 진행한다.
```
- 코드 컨벤션을 점검하고 수정한다.
- 스케줄링 CRUD API 관련 버그를 수정한다.
- 스케줄링 serializer를 구현한다.
- 의존성이 걸린 작업의 실존 여부를 검사하는 로직을 추가한다.
- job이 실패 처리 됐을 때의 retry 로직을 수정한다.
- `WorkflowManager` 클래스 내 `history_repo` 중복 인자를 제거한다.
- Redis host와 port를 환경변수로 관리한다.
```

## 아키텍쳐
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/5e8c4a88-2af5-4781-b9fe-e074a6f5dc98)

## 모델 및 ERD
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/4cdf06a4-cae2-4bdb-b9c8-2709f0c67cab)

- Workflow는 사용자가 정의한 워크플로우를 저장한다.
- Job은 워크플로우 내부에서 정의한 각각의 작업을 저장한다.
- History는 워크플로우를 실행한 기록을 저장한다.
- Scheduling은 워크플로우를 지정된 시간과 횟수만큼 실행하기 위한 스케줄링 정보를 저장한다.

## 기능별 시퀀스 다이어그램

### 스케줄링 실행 로직
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/837ef6f0-d12c-498c-8deb-272f2c9cb512)

### 워크플로우 실행 로직
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/d234fcf5-233f-42d1-a067-9157711efd88)

### 의존성 알고리즘 로직
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/84d89517-b5e7-4251-88bb-2efcb92c392d)

### 워크플로우 성공/실패 분기로직

#### 작업 실행 성공 로직
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/a1e019f8-4857-4308-87aa-a981ef83a40a)

#### 작업 실행 실패 로직
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/4ce463d2-edfc-4b26-9e01-313b5aa3ed29)

## API 명세서
![image](https://github.com/workflow-engine-project/workflow-engine/assets/41356191/94556c54-9806-4a90-9ff9-5bf08dabcbb7)

Swagger를 통해 구성한 API 테스트 페이지(/swagger)에서 API의 입력값을 넣어 출력값을 확인할 수 있습니다.

|이름|URL|Method|
|---|---|---|
|Workflow|||
|워크플로우 생성|workflow/|POST|
|전체 워크플로우 리스트 조회|workflow/|GET|
|워크플로우 조회|workflow/\<uuid:workflow_uuid>/|GET|
|워크플로우 수정|workflow/\<uuid:workflow_uuid>/|PATCH|
|워크플로우 삭제|workflow/\<uuid:workflow_uuid>/|DELETE|
|워크플로우 실행|workflow/\<uuid:workflow_uuid>/execute|GET|
|Scheduling|||
|스케줄링 생성|scheduling/|POST|
|전체 스케줄링 리스트 조회|scheduling/|GET|
|스케줄링 조회|scheduling/\<uuid:scheduling_uuid>/|GET|
|스케줄링 수정|scheduling/\<uuid:scheduling_uuid>/|PATCH|
|스케줄링 삭제|scheduling/\<uuid:scheduling_uuid>/|DELETE|
|워크플로우 별 스케줄링 리스트 조회|scheduling/workflow/\<uuid:workflow_uuid>|GET|
|스케줄링 활성화|scheduling/\<uuid:scheduling_uuid>/execute|POST|
|스케줄링 비활성화|scheduling/\<uuid:scheduling_uuid>/deactive|POST|

## 파일 트리
```
📦 workflow-engine
┣ 📂 workflow_engine
     ┣📂 project_apps
         ┣📂 api
             ┣📜 serializers.py
             ┣📜 urls.py
             ┣📜 views.py
         ┣📂 engine
             ┣📜 job_dependency.py
             ┣📜 job_execute.py
             ┣📜 job_terminate.py
             ┣📜 scheduling_execute.py
             ┣📜 tasks_manager.py
         ┣📂 migrations
         ┣📂 models
             ┣📜 cache.py
             ┣📜 history.py
             ┣📜 job.py
             ┣📜 scheduling.py
             ┣📜 workflow.py
         ┣📂 repository
             ┣📜 history_repository.py
             ┣📜 job_repository.py
             ┣📜 scheduling_repository.py
             ┣📜 workflow_repository.py
         ┣📂 service
             ┣📜 lock_utils.py
             ┣📜 scheduling_service.py
             ┣📜 workflow_manage.py
             ┣📜 workflow_service.py
         ┣📜 constants.py
     ┣📂 workflow_engine
         ┣📜 celery.py
         ┣📜 settings.py
         ┣📜 urls.py
         ┣📜 wsgi.py
     ┣📜 manage.py
┣ 📜 Dockerfile
┣ 📜 README.md
┣ 📜 docker-compose.yml
┣ 📜 requirements.txt
```
