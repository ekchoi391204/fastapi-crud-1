# FastAPI CRUD System

FastAPI와 MySQL 8.0으로 구성한 로그인 기반 사용자 CRUD 예제입니다.

## 컨테이너 이미지

- 애플리케이션: `hifrodo/crud-app:1.0`
- 데이터베이스: `hifrodo/crud-db:1.0`

애플리케이션 이미지는 `app/Dockerfile`, DB 이미지는
`db/Dockerfile`로 빌드됩니다. DB 초기 스키마와 샘플 데이터는
`db/init.sql`에 정의되어 있습니다.

## 실행

```powershell
Copy-Item .env.example .env
docker compose up --build -d
```

브라우저에서 <http://localhost:8080/member>에 접속합니다.

- 기본 아이디: `admin`
- 기본 비밀번호: `frodo1234`
- API 문서: <http://localhost:8080/docs>
- 회원가입: <http://localhost:8080/register>
- 사용자 관리: <http://localhost:8080/member>
- 사용자 CRUD API: <http://localhost:8080/api/member>
- 외부 상태 페이지: <http://localhost:8080/status>
- 헬스 API: <http://localhost:8080/health>

초기 실행 시 `db/init.sql`에서 테이블과 4명의 샘플 데이터를 생성합니다.
관리자 계정은 평문 비밀번호가 DB 초기화 SQL에 저장되지 않도록 웹 앱이 시작될
때 Argon2 해시로 생성합니다.

`/status`와 `/health`는 로그인이 필요 없는 외부 공개 경로입니다. `/health`는
FastAPI와 MySQL 연결을 함께 검사하며 모두 정상이면 HTTP `200 OK`, DB 연결에
실패하면 HTTP `503 Service Unavailable`을 반환합니다.

`/register`에서 새 계정을 만들 수 있으며 비밀번호는 Argon2 해시로 저장됩니다.
가입이 완료되면 HttpOnly 인증 쿠키가 발급되어 자동으로 로그인됩니다.

이미지를 개별적으로 빌드하려면 다음 명령을 사용합니다.

```powershell
docker build -f app/Dockerfile -t hifrodo/crud-app:1.0 .
docker build -t hifrodo/crud-db:1.0 .\db
```

## 환경변수

`.env.example`을 `.env`로 복사한 뒤 값을 변경할 수 있습니다. 기본 DB 이름은
`frodo`, 기본 DB 사용자 비밀번호는 `Frodo5020!!`이며 컨테이너 내부 DB 호스트는
Compose 서비스 이름인 `mydb-svc`입니다.
대시보드 하단에 표시되는 서버명은 `SERVER_NAME`으로 변경할 수 있습니다.
서버 IP는 자동 감지되며 외부 IP를 직접 표시하려면 `SERVER_IP`에 지정합니다.

대시보드 상단 표시 버전은 `app/static/index.html`에서 직접 수정합니다.

```html
<span id="version" class="version">Version 1.0.0</span>
```
서비스 이름 자체를 변경하면 `docker-compose.yml`의 서비스 키와 `MYSQL_HOST`를
함께 변경해야 합니다.

운영 환경에서는 반드시 `SECRET_KEY`, `ADMIN_PASSWORD`, DB 비밀번호를 변경하고
HTTPS 사용 시 `COOKIE_SECURE=true`로 설정하세요.

## 관리 명령

```powershell
docker compose ps
docker compose logs -f web
docker compose down
```

DB 데이터는 `mysql_data` 볼륨에 유지됩니다. `db/init.sql`과 환경변수의 초기
계정/DB 값은 빈 볼륨에서만 적용되며 이미 생성된 볼륨에는 소급 적용되지 않습니다.
