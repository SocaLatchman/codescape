from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from typing import Optional, List
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


class User(SQLModel, table=True):
    __tablename__ = 'users'
    user_id: Optional[int] = Field(default=None, primary_key=True)
    handle: str
    email: str
    password: str
    bio: str
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

class Friend(SQLModel, table=True):
    __tablename__ = 'friends'
    friend_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    friend_user_id: int = Field(foreign_key="users.user_id")
    status: str = Field(default='active')
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="friends", sa_relationship_kwargs={'foreign_keys': '[Friend.user_id]'})
    friend_user: Optional[User] = Relationship(back_populates="friends_of", sa_relationship_kwargs={'foreign_keys': '[Friend.friend_user_id]'})

class Skill(SQLModel, table=True):
    __tablename__ = 'skills'
    skill_id: Optional[int] = Field(default=None, primary_key=True)
    skill: str
    
    # Relationships
    user_skills: List["UserSkill"] = Relationship(back_populates="skill")

class UserSkill(SQLModel, table=True):
    __tablename__ = 'user_skills'
    user_skills_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    skill_id: int = Field(foreign_key="skills.skill_id")
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="user_skills")
    skill: Optional[Skill] = Relationship(back_populates="user_skills")

class Category(SQLModel, table=True):
    __tablename__ = 'categories'
    category_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category_color: str
    
    # Relationships
    topics: List["Topic"] = Relationship(back_populates="category")

class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    tag_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    tag_color: str
    
    # Relationships
    topic_tags: List["TopicTag"] = Relationship(back_populates="tag")

class Topic(SQLModel, table=True):
    __tablename__ = 'topics'
    topic_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: str
    likes: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    category_id: int = Field(foreign_key="categories.category_id")
    user_id: int = Field(foreign_key="users.user_id")
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="topics")
    category: Optional[Category] = Relationship(back_populates="topics")
    topic_tags: List["TopicTag"] = Relationship(back_populates="topic")
    replies: List["Reply"] = Relationship(back_populates="topic")
    forums: List["Forum"] = Relationship(back_populates="topic")

class TopicTag(SQLModel, table=True):
    __tablename__ = 'topic_tags'
    topic_tags_id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topics.topic_id")
    tag_id: int = Field(foreign_key="tags.tag_id")
    
    # Relationships
    topic: Optional[Topic] = Relationship(back_populates="topic_tags")
    tag: Optional[Tag] = Relationship(back_populates="topic_tags")

class Forum(SQLModel, table=True):
    __tablename__ = 'forums'
    forum_id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topics.topic_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    topic: Optional[Topic] = Relationship(back_populates="forums")

class Reply(SQLModel, table=True):
    __tablename__ = 'replies'
    reply_id: Optional[int] = Field(default=None, primary_key=True)
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    likes: int = Field(default=0)
    topic_id: int = Field(foreign_key="topics.topic_id")
    user_id: int = Field(foreign_key="users.user_id")
    
    # Relationships
    topic: Optional[Topic] = Relationship(back_populates="replies")
    user: Optional[User] = Relationship(back_populates="replies")
