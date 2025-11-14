# getCoinNoticeBe

Upbit 공지사항을 수집하여 Supabase에 저장하는 FastAPI 서버

## 로컬 개발 환경 설정

```bash
git init

pip install uv
uv venv
.venv\Scripts\activate
uv pip install fastapi uvicorn python-dotenv supabase requests
uv run uvicorn main:app --reload
```

## 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력:

```env
VITE_SUPABASE_URL=your_supabase_url_here
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

## CloudType 배포

1. GitHub에 코드 푸시
2. CloudType 프로젝트 생성
3. 환경 변수 설정:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
4. 시작 명령어: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 빌드 명령어: `pip install -r requirements.txt`

## API 엔드포인트

- `GET /` - 헬스 체크
- `GET /list` - 저장된 공지사항 목록 조회
- `POST /getNotice` - Upbit 공지사항 수집 및 저장
