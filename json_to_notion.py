import json
import os
import sys
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 값 가져오기
notion_api_token = os.getenv("NOTION_API_TOKEN")
database_id = os.getenv("NOTION_DATABASE_ID")

# 환경 변수 값 출력 (디버깅용)
print("NOTION_API_TOKEN:", notion_api_token)
print("NOTION_DATABASE_ID:", database_id)

# 노션 API 클라이언트 설정
notion = Client(auth=notion_api_token)

# 노션 `status` 필드 옵션 가져오기 함수
def get_status_options(database_id):
    database = notion.databases.retrieve(database_id=database_id)
    properties = database["properties"]
    status_options = {}

    for prop_name, prop_info in properties.items():
        if prop_info["type"] == "status":
            for option in prop_info["status"]["options"]:
                status_options[option["name"]] = option["color"]

    return status_options

# 노션 `status` 필드 옵션 가져오기
status_options = get_status_options(database_id)
print(status_options)

# JSON 파일에서 데이터 읽기
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
except Exception as e:
    print(f"JSON 파일을 읽는 중 오류가 발생했습니다: {e}")
    sys.exit(1)

# 날짜를 하루 미루는 함수
def postpone_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    new_date_obj = date_obj + timedelta(days=1)
    return new_date_obj.strftime("%Y-%m-%d")

# 커밋 리소스 변환 함수
def transform_commit_resource(resource):
    if resource in status_options:
        return {"name": resource}
    return {"name": resource, "color": "default"}

# 책 이름 변환 함수
def transform_book_name(book_name):
    book_mapping = {
        "그림과 실습으로 배우는 도커 & 쿠버네티스": "docker&cdk8s",
        "그림으로 배우는 네트워크 원리": "네트워크 원리",
        "기초가 든든한 데이터베이스": "데이터 베이스 기초",
        "IT 엔지니어를 위한 네트워크 입문": "네트워크 입문",
        "실전 카프카 개발부터 운영까지": "kafka"
    }
    return book_mapping.get(book_name, book_name)

# 책 변환 함수
def transform_book(book):
    transformed_book_name = transform_book_name(book)
    if transformed_book_name in status_options:
        return {"name": transformed_book_name}
    return {"name": transformed_book_name, "color": "gray"}

# JSON 데이터를 노션 데이터베이스에 추가하는 함수
def add_data_to_notion(database_id, data):
    for item in reversed(data):  # 데이터를 역순으로 추가
        try:
            response = notion.pages.create(
                parent={"database_id": database_id},
                properties={
                    "Date": {
                        "date": {
                            "start": postpone_date(item["Date"])  # 날짜를 하루 미룸
                        }
                    },
                    "Study Section": {
                        "title": [
                            {
                                "text": {
                                    "content": item["Study Section"]
                                }
                            }
                        ]
                    },
                    "Book": {
                        "status": transform_book(item["Book"])
                    },
                    "Commit Resource": {
                        "status": transform_commit_resource(item["Commit Resource"])
                    },
                    "Completed": {
                        "checkbox": item["Completed"]
                    }
                }
            )
            print("성공적으로 추가되었습니다:", response)
        except Exception as e:
            print("오류가 발생했습니다:", e)
            sys.exit(1)

# JSON 데이터를 노션 데이터베이스에 추가
add_data_to_notion(database_id, json_data)
