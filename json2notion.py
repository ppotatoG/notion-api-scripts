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

# 노션 API 클라이언트 설정
notion = Client(auth=notion_api_token)

# 필요한 `status` 옵션
required_commit_resource_options = {
    "default": "default",
    "Docker 공식 튜토리얼": "gray",
    "FreeCodeCamp": "brown",
    "Kubernetes": "orange",
    "프로그래머스 js 알고리즘": "pink",
    "프로그래머스 sql": "green",
    "Cisco Networking Academy": "blue",
    "Docker": "yellow"
}

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

# JSON 데이터를 노션 데이터베이스에 추가하는 함수
def add_data_to_notion(database_id, data):
    for item in reversed(data):  # 데이터를 역순으로 추가
        try:
            if item["Commit Resource"] not in required_commit_resource_options:
                print(f"오류: Commit Resource 옵션 '{item['Commit Resource']}'가 존재하지 않습니다.")
                return  # 없는 속성이면 함수 종료

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
                    "Commit Resource": {
                        "status": {"name": item["Commit Resource"]}
                    },
                    "Book": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": item["Book"]
                                }
                            }
                        ]
                    },
                    "Completed": {
                        "checkbox": item["Completed"]
                    }
                }
            )
            print("성공적으로 추가되었습니다:", response)
        except Exception as e:
            print("오류가 발생했습니다:", e)
            print(f"에러가 발생한 데이터 항목: {item}")  # 에러가 발생한 데이터 항목을 출력
            sys.exit(1)

# JSON 데이터를 노션 데이터베이스에 추가
add_data_to_notion(database_id, json_data)
