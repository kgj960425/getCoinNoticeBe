import os
from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv
import requests
import time

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def read_root():
    return {"message": "ok"}

@app.get("/list")
def list_data():
    res = supabase.table("TB_PT_NOTICE_LOG").select("*").execute()
    return res.data

@app.post("/getNotice")
def add():
    start_time = time.time()
    print(f"API 시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    url = "https://api-manager.upbit.com/api/v1/announcements"
    params = {
        "os": "web",
        "page": 1,
        "per_page": 20,
        "category": "trade",
    }
    resp = requests.get(url, params=params)

    # 응답 상태 확인
    if resp.status_code != 200:
        print(f"API 오류: {resp.status_code}")
        print(f"응답 내용: {resp.text}")
        return {"message": "error", "status_code": resp.status_code, "error": resp.text}

    try:
        json_data = resp.json()
    except Exception as e:
        print(f"JSON 파싱 오류: {e}")
        print(f"응답 내용: {resp.text}")
        return {"message": "error", "error": "JSON parsing failed", "response": resp.text}

    print(json_data)
    notices = json_data.get("data", {}).get("notices", [])

    # 기존 DB에서 notice_id 조회
    existing_notices = supabase.table("TB_PT_NOTICE_LOG").select("notice_id").execute()
    existing_notice_ids = {notice["notice_id"] for notice in existing_notices.data}

    # 새로운 공지만 적재
    inserted_count = 0
    for data in notices:
        notice_id = data["id"]
        if notice_id not in existing_notice_ids:
            print(f"새 공지 적재: {notice_id}, {data.get('title', '')}")
            # 테이블 구조에 맞게 데이터 매핑
            insert_data = {
                "notice_id": notice_id,
                "title": data.get("title"),
                "new_yn": data.get("new_yn", False),
                "payload": data  # 전체 데이터를 JSON으로 저장
            }
            res = supabase.table("TB_PT_NOTICE_LOG").insert(insert_data).execute()
            inserted_count += 1
        else:
            print(f"이미 존재하는 공지: {notice_id}, {data.get('title', '')}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"API 종료 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"총 소요 시간: {elapsed_time:.2f}초")

    return {"message": "ok", "inserted": inserted_count, "total": len(notices), "elapsed_time": f"{elapsed_time:.2f}초"}
