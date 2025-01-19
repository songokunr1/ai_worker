from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
DATABASE_URL = "sqlite:///./tags.db"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # Replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    topic = relationship("Topic", back_populates="tags")

Topic.tags = relationship("Tag", back_populates="topic", cascade="all, delete")

Base.metadata.create_all(bind=engine)

from fastapi import Depends
from pydantic import BaseModel

class TagCreate(BaseModel):
    tag: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/topics/")
def get_topics(db=Depends(get_db)):
    topics = db.query(Topic).all()
    return [{"id": t.id, "name": t.name, "tags": [tag.name for tag in t.tags]} for t in topics]

@app.post("/topics/{topic_id}/tags")
def add_tag(topic_id: int, tag: TagCreate, db=Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    new_tag = Tag(name=tag.tag, topic_id=topic_id)
    db.add(new_tag)
    db.commit()
    return {"msg": "Tag added"}

@app.delete("/topics/{topic_id}/tags/{tag_name}")
def delete_tag(topic_id: int, tag_name: str, db=Depends(get_db)):
    tag = db.query(Tag).filter(Tag.topic_id == topic_id, Tag.name == tag_name).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return {"msg": "Tag deleted"}

from pydantic import BaseModel

class TopicCreate(BaseModel):
    name: str

@app.post("/topics/")
def create_topic(topic: TopicCreate, db=Depends(get_db)):
    new_topic = Topic(name=topic.name)
    db.add(new_topic)
    db.commit()
    return {"msg": "Topic created"}
