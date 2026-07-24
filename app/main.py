import time
import socket
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.auth import (
    COOKIE_NAME,
    create_access_token,
    current_account,
    hash_password,
    verify_password,
)
from app.config import settings
from app.database import Base, SessionLocal, engine, get_db
from app.models import Account, Person
from app.schemas import (
    LoginRequest,
    PersonCreate,
    PersonList,
    PersonResponse,
    PersonUpdate,
    RegisterRequest,
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


def initialize_database() -> None:
    last_error: Exception | None = None
    for _ in range(30):
        try:
            Base.metadata.create_all(bind=engine)
            with SessionLocal() as db:
                db.execute(
                    text(
                        "UPDATE people SET gender = 'Female' "
                        "WHERE gender NOT IN ('Male', 'Female')"
                    )
                )
                if not db.scalar(
                    select(Account).where(Account.username == settings.admin_username)
                ):
                    db.add(
                        Account(
                            username=settings.admin_username,
                            password_hash=hash_password(settings.admin_password),
                        )
                    )
                if (db.scalar(select(func.count(Person.id))) or 0) == 0:
                    db.add_all(
                        [
                            Person(name="홍길동", gender="Male", age=25),
                            Person(name="김철수", gender="Male", age=32),
                            Person(name="이영희", gender="Female", age=28),
                            Person(name="박지민", gender="Female", age=40),
                        ]
                    )
                db.commit()
            return
        except OperationalError as exc:
            last_error = exc
            time.sleep(2)
    raise RuntimeError("MySQL에 연결할 수 없습니다.") from last_error


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/member")


@app.get("/member", include_in_schema=False)
def member_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/login", include_in_schema=False)
def login_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "login.html")


@app.get("/register", include_in_schema=False)
def register_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "register.html")


@app.get("/status", include_in_schema=False)
def status_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "health.html")


@app.get("/healthcheck", include_in_schema=False)
def healthcheck_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "health.html")


@app.get("/health", response_class=JSONResponse)
def health() -> JSONResponse:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unavailable",
                "http_status": "503 Service Unavailable",
                "app": "ok",
                "database": "error",
                "version": settings.app_version,
            },
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "ok",
            "http_status": "200 OK",
            "app": "ok",
            "database": "ok",
            "version": settings.app_version,
        },
    )


@app.post("/api/auth/login")
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    account = db.scalar(select(Account).where(Account.username == payload.username))
    if not account or not verify_password(payload.password, account.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
        )
    response.set_cookie(
        COOKIE_NAME,
        create_access_token(account),
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )
    return {"username": account.username}


@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> dict[str, str | int]:
    username = payload.username.strip()
    if db.scalar(select(Account).where(Account.username == username)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 아이디입니다.",
        )

    account = Account(
        username=username,
        password_hash=hash_password(payload.password),
    )
    db.add(account)
    try:
        db.commit()
        db.refresh(account)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 아이디입니다.",
        )

    response.set_cookie(
        COOKIE_NAME,
        create_access_token(account),
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )
    return {"id": account.id, "username": account.username}


@app.post("/api/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    response.delete_cookie(COOKIE_NAME, path="/")


@app.get("/api/auth/me")
def me(account: Account = Depends(current_account)) -> dict[str, str | int]:
    return {"id": account.id, "username": account.username}


@app.get("/api/people", response_model=PersonList, include_in_schema=False)
@app.get("/api/member", response_model=PersonList, include_in_schema=False)
@app.get("/api/members", response_model=PersonList)
def list_people(
    q: str = Query(default="", max_length=100),
    account: Account = Depends(current_account),
    db: Session = Depends(get_db),
) -> PersonList:
    del account
    statement = select(Person)
    count_statement = select(func.count(Person.id))
    if q.strip():
        pattern = f"%{q.strip()}%"
        statement = statement.where(Person.name.like(pattern))
        count_statement = count_statement.where(Person.name.like(pattern))
    people = db.scalars(statement.order_by(Person.id.desc())).all()
    total = db.scalar(count_statement) or 0
    return PersonList(items=list(people), total=total)


@app.post(
    "/api/people",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
@app.post(
    "/api/member",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
@app.post(
    "/api/members",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_person(
    payload: PersonCreate,
    account: Account = Depends(current_account),
    db: Session = Depends(get_db),
) -> Person:
    del account
    person = Person(**payload.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def get_person_or_404(person_id: int, db: Session) -> Person:
    person = db.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return person


@app.put(
    "/api/member/{person_id}",
    response_model=PersonResponse,
    include_in_schema=False,
)
@app.put(
    "/api/people/{person_id}",
    response_model=PersonResponse,
    include_in_schema=False,
)
@app.put("/api/members/{person_id}", response_model=PersonResponse)
def update_person(
    person_id: int,
    payload: PersonUpdate,
    account: Account = Depends(current_account),
    db: Session = Depends(get_db),
) -> Person:
    del account
    person = get_person_or_404(person_id, db)
    for key, value in payload.model_dump().items():
        setattr(person, key, value)
    db.commit()
    db.refresh(person)
    return person


@app.delete(
    "/api/member/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
@app.delete(
    "/api/people/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
@app.delete("/api/members/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: int,
    account: Account = Depends(current_account),
    db: Session = Depends(get_db),
) -> None:
    del account
    person = get_person_or_404(person_id, db)
    db.delete(person)
    db.commit()


@app.get("/api/system/meta")
def system_meta(
    request: Request,
    account: Account = Depends(current_account),
) -> dict[str, str]:
    del account
    client_ip = request.client.host if request.client else "-"
    try:
        detected_server_ip = socket.gethostbyname(socket.gethostname())
    except OSError:
        detected_server_ip = "-"
    return {
        "server_name": socket.gethostname(),
        "server_ip": settings.server_ip or detected_server_ip,
        "version": settings.app_version,
        "ip": client_ip,
        "xff": request.headers.get("x-forwarded-for", "-"),
    }
