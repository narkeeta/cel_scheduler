from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import settings
import json

class ScheduledEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    duration: str | None = None
    time: str | None = None
    type: str | None = None
    days: str | None = None


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def hello():
    return "Hello, Docker!"


@app.post("/event/add")
def create_event(event: ScheduledEvent):
    event_days = json.loads(event.days)

    with Session(engine) as session:
        for day in event_days:
            existing_event = session.exec(
                select(ScheduledEvent).where(
                    ScheduledEvent.days.contains(str(day)),
                    ScheduledEvent.time == event.time
                )
            ).first()
            if existing_event:
                raise HTTPException(status_code=400, detail="Event at that time and day already exists")

        session.add(event)
        session.commit()
        session.refresh(event)
        return event


@app.get("/events/list")
def read_events():
    with Session(engine) as session:
        events = session.exec(select(ScheduledEvent)).all()
        return events


@app.delete("/event/delete/{event_id}")
def delete_event(event_id: int):
    with Session(engine) as session:
        event = session.get(ScheduledEvent, event_id)
        session.delete(event)
        session.commit()
        return {"message": "Event deleted successfully"}
