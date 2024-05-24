import json
from datetime import datetime, timedelta

def mrkd2json(inp):
    lines = inp.strip().split('\n')
    ret = []
    keys = []

    # 시작 날짜를 내일로 설정
    current_date = datetime.now() + timedelta(days=1)

    # 커밋 리소스 변환 함수
    def transform_commit_resource(resource):
        if "Cisco Networking Academy" in resource:
            return "Cisco Networking Academy"
        elif "LeetCode SQL 문제 1개 풀기" in resource:
            return "프로그래머스 sql"
        elif "프로그래머스 알고리즘 문제 1개 풀기" in resource:
            return "프로그래머스 js 알고리즘"
        elif "Kubernetes 공식 튜토리얼 섹션 1개 학습 및 실습" in resource:
            return "Kubernetes"
        elif "FreeCodeCamp 백엔드 개발 강의 1개 섹션" in resource:
            return "FreeCodeCamp"
        return resource

    # 책 이름 변환 함수
    def transform_book_name(book_name):
        book_mapping = {
            "그림과 실습으로 배우는 도커 & 쿠버네티스": "docker&cdk8s",
            "그림으로 배우는 네트워크 원리": "네트워크 원리",
            "기초가 든든한 데이터베이스": "데이터 베이스 기초",
            "IT 엔지니어를 위한 네트워크 입문": "네트워크 입문",
            "실전 카프카 개발부터 운영까지": "kafka",
            "면접을 위한 CS 전공지식 노트": "CS 전공지식"
        }
        return book_mapping.get(book_name, book_name)

    # 열 제목 파싱
    for i, l in enumerate(lines):
        if i == 0:
            keys = [key.strip() for key in l.split('|') if key.strip()]
        elif i == 1:
            continue
        else:
            values = [value.strip() for value in l.split('|') if value.strip()]
            if len(values) == len(keys):
                record = {keys[j]: values[j] for j in range(len(keys))}
                # 커밋 리소스 변환
                record['커밋 리소스'] = transform_commit_resource(record['커밋 리소스'])
                # 완료 여부를 불리언 값으로 설정
                record['완료 여부'] = False
                # 책 이름 변환
                record['책'] = transform_book_name(record['책'])
                # 키를 노션 데이터베이스 속성 이름으로 변경
                transformed_record = {
                    "Date": current_date.strftime("%Y-%m-%d"),  # 날짜를 내일부터 시작
                    "Book": record['책'],
                    "Study Section": record['학습 섹션'],
                    "Commit Resource": record['커밋 리소스'],
                    "Completed": record['완료 여부']
                }
                ret.append(transformed_record)
                current_date += timedelta(days=1)

    return json.dumps(ret, indent=4, ensure_ascii=False)

my_str='''| 책                                                      | 학습 섹션                             | 커밋 리소스                                       | 완료 여부 |
          |------------|---------------------------------------------------------|---------------------------------------|--------------------------------------------------|----------|
          | IT 엔지니어를 위한 네트워크 입문                         | 네트워크 기본 개념 (1장)              | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 네트워크 기본 개념 (1장)              | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 프로토콜과 OSI 7계층 (2장)            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 프로토콜과 OSI 7계층 (2장)            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | TCP/IP 모델 (3장)                     | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 네트워크 장비와 구성 (4장)            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 네트워크 보안 (5장)                   | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 무선 네트워크 (6장)                   | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 클라우드 네트워크 (7장)               | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 복습 및 실습 문제 풀이                | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 복습 및 실습 문제 풀이                | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 복습 및 실습 문제 풀이                | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 복습 및 실습 문제 풀이                | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 복습 및 실습 문제 풀이                | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | IT 엔지니어를 위한 네트워크 입문                         | 복습 및 실습 문제 풀이                | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 기초가 든든한 데이터베이스                               | 데이터베이스 기본 개념 (1장)          | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 데이터베이스 기본 개념 (1장)          | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 데이터 모델링 (2장)                   | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 데이터 모델링 (2장)                   | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | SQL 기본 문법 (3장)                   | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | SQL 기본 문법 (3장)                   | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 데이터베이스 설계 (4장)               | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 고급 SQL (5장)                        | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 트랜잭션과 동시성 제어 (6장)          | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 데이터베이스 최적화 (7장)             | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 복습 및 실습 문제 풀이                | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 복습 및 실습 문제 풀이                | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 복습 및 실습 문제 풀이                | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 복습 및 실습 문제 풀이                | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 기초가 든든한 데이터베이스                               | 복습 및 실습 문제 풀이                | LeetCode SQL 문제 1개 풀기 (30분)                 | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 네트워크 개요 (1장)               | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | OSI 7계층 (2장)                   | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | TCP/IP 모델 (3장)                 | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 주요 프로토콜 (4장)               | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 라우팅 (5장)                      | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 네트워크 보안 (6장)               | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 무선 네트워크 (7장)               | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 네트워크 관리 (8장)               | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 복습 및 실습 문제 풀이            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 복습 및 실습 문제 풀이            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 복습 및 실습 문제 풀이            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 복습 및 실습 문제 풀이            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 복습 및 실습 문제 풀이            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 복습 및 실습 문제 풀이            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 그림으로 배우는 네트워크 원리       | 복습 및 실습 문제 풀이            | Cisco Networking Academy 강의 수강 및 실습 (30분) | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 데이터 구조 (1장)                 | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 알고리즘 (2장)                    | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 운영체제 (3장)                    | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 네트워크 (4장)                    | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 데이터베이스 (5장)                | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 시스템 설계 (6장)                 | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 보안 (7장)                        | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 면접 문제 풀이 (8장)              | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 모의 면접 및 복습                 | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 모의 면접 및 복습                 | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 모의 면접 및 복습                 | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 모의 면접 및 복습                 | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 모의 면접 및 복습                 | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 면접을 위한 CS 전공지식 노트        | 모의 면접 및 복습                 | 프로그래머스 알고리즘 문제 1개 풀기 (30분)       | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 도커 기본 개념 (1장)               | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 도커 이미지 생성 (2장)              | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 도커 컨테이너 관리 (3장)            | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 도커 네트워크 (4장)                 | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 도커 볼륨 (5장)                     | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 쿠버네티스 기본 개념 (6장)           | Kubernetes 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 쿠버네티스 배포 (7장)                | Kubernetes 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 쿠버네티스 서비스와 인그레스 (8장)   | Kubernetes 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 쿠버네티스 설정 및 보안 (9장)        | Kubernetes 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 실습 프로젝트 및 복습               | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 실습 프로젝트 및 복습               | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 실습 프로젝트 및 복습               | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 실습 프로젝트 및 복습               | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 그림과 실습으로 배우는 도커 & 쿠버네티스 | 실습 프로젝트 및 복습               | Docker 공식 튜토리얼 섹션 1개 학습 및 실습 (30분) | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 카프카 개요 (1장)                   | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 카프카 설치 및 설정 (2장)            | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 프로듀서와 컨슈머 (3장)              | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 카프카 스트림즈 (4장)                | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 카프카 커넥트 (5장)                  | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 카프카 보안 (6장)                    | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 카프카 모니터링 (7장)                | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 카프카 튜닝 (8장)                    | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 실습 프로젝트 및 복습                | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 실습 프로젝트 및 복습                | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 실습 프로젝트 및 복습                | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 실습 프로젝트 및 복습                | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 실습 프로젝트 및 복습                | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |
          | 실전 카프카 개발부터 운영까지           | 실습 프로젝트 및 복습                | FreeCodeCamp 백엔드 개발 강의 1개 섹션 (30분)    | [ ]      |'''

# JSON 데이터로 변환
json_data = mrkd2json(my_str)

# JSON 데이터를 파일에 저장
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
