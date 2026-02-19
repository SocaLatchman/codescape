from sqlmodel import SQLModel, Field, Relationship, Session, select
from typing import Optional, List, ClassVar
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from uuid import uuid4, UUID

class BaseModel(SQLModel):
    _engine: ClassVar = None

    @classmethod
    def set_engine(cls, db_engine):
        cls._engine = db_engine
    
    @classmethod
    def get_session(cls):
        return Session(cls._engine)


class User(BaseModel, table=True):
    __tablename__ = 'users'
    user_id: Optional[int] = Field(default=None, primary_key=True)
    public_id: UUID = Field(default_factory=uuid4, unique=True, index=True)
    handle: str
    email: str
    password: str
    bio: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    image: str
    status: str = Field(default='visible')
    experience: int
    
    # Relationships
    friends: List["Friend"] = Relationship(back_populates="user")
    friends_of: List["Friend"] = Relationship(back_populates="friend_user")
    topics: List["Topic"] = Relationship(back_populates="user")
    user_skills: List["UserSkill"] = Relationship(back_populates="user")
    replies: List["Reply"] = Relationship(back_populates="user")

class Friend(BaseModel, table=True):
    __tablename__ = 'friends'
    friend_id: Optional[int] = Field(default=None, primary_key=True)
    public_id: UUID = Field(default_factory=uuid4, unique=True, index=True)
    user_id: int = Field(foreign_key="users.user_id")
    status: str = Field(default='active')
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="friends")
    friend_user: Optional[User] = Relationship(back_populates="friends_of")

class Skill(BaseModel, table=True):
    __tablename__ = 'skills'
    skill_id: Optional[int] = Field(default=None, primary_key=True)
    skill: str
    
    # Relationships
    user_skills: List["UserSkill"] = Relationship(back_populates="skill")

class UserSkill(BaseModel, table=True):
    __tablename__ = 'user_skills'
    user_skills_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    skill_id: int = Field(foreign_key="skills.skill_id")
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="user_skills")
    skill: Optional[Skill] = Relationship(back_populates="user_skills")

class Category(BaseModel, table=True):
    __tablename__ = 'categories'
    category_id: Optional[int] = Field(default=None, primary_key=True)
    public_id: UUID = Field(default_factory=uuid4, unique=True, index=True)
    name: str
    category_color: str
    
    # Relationships
    topics: List["Topic"] = Relationship(back_populates="category")

    def get_categories():
        with Category.get_session() as session:
            return [category.model_dump() for category in session.exec(select(Category)).all()]

class Tag(BaseModel, table=True):
    __tablename__ = 'tags'
    tag_id: Optional[int] = Field(default=None, primary_key=True)
    public_id: UUID = Field(default_factory=uuid4, unique=True, index=True)
    name: str
    tag_color: str
    
    # Relationships
    topic_tags: List["TopicTag"] = Relationship(back_populates="tag")

    def get_all_tags():
        with Tag.get_session() as session:
            return [tag.model_dump() for tag in session.exec(select(Tag)).all()]

class Topic(BaseModel, table=True):
    __tablename__ = 'topics'
    topic_id: Optional[int] = Field(default=None, primary_key=True)
    public_id: UUID = Field(default_factory=uuid4, unique=True, index=True)
    title: str
    body: str
    likes: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    category_id: int = Field(foreign_key="categories.category_id")
    user_id: int = Field(foreign_key="users.user_id")
    views: int = Field(default=0)

    def get_forum(self):    
        with self.get_session() as session: 
           statement = (
              select(Topic, User.image, User.handle, Category)
              .where(Topic.user_id == User.user_id)         
           )
           results = session.exec(statement).all()
           return [topic._mapping for topic in results]

    def get_topic(self, id):
        with self.get_session() as session:
            result = session.get(Topic, id)
            return result.model_dump()

    @classmethod
    def increase_view_count(cls, id):
        with cls.get_session() as session:
            result = session.get(Topic, id)
            result.views += 1
            session.add(result)
            session.commit()
            session.refresh(result)
        return result.views


    
    # Relationships
    user: Optional[User] = Relationship(back_populates="topics")
    category: Optional[Category] = Relationship(back_populates="topics")
    topic_tags: List["TopicTag"] = Relationship(back_populates="topic")
    replies: List["Reply"] = Relationship(back_populates="topic")

class TopicTag(SQLModel, table=True):
    __tablename__ = 'topic_tags'
    topic_tags_id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topics.topic_id")
    tag_id: int = Field(foreign_key="tags.tag_id")
    
    # Relationships
    topic: Optional[Topic] = Relationship(back_populates="topic_tags")
    tag: Optional[Tag] = Relationship(back_populates="topic_tags")

class Reply(BaseModel, table=True):
    __tablename__ = 'replies'
    reply_id: Optional[int] = Field(default=None, primary_key=True)
    public_id: UUID = Field(default_factory=uuid4, unique=True, index=True)
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    likes: int = Field(default=0)
    topic_id: int = Field(foreign_key="topics.topic_id")
    user_id: int = Field(foreign_key="users.user_id")
    
    # Relationships
    topic: Optional[Topic] = Relationship(back_populates="replies")
    user: Optional[User] = Relationship(back_populates="replies")

