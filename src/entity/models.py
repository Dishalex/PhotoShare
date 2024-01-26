from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, Boolean, func, Table, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
import enum


class Base(DeclarativeBase):
    pass


image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Role(enum.Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(25), nullable=True)
    last_name = Column(String(25), nullable=True)
    email = Column(String(50), nullable=False, unique=True)
    sex = Column(String(10), nullable=True)
    password = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    refresh_token = Column(String(255))
    confirmed = Column(Boolean, default=False)
    role = Column(Enum(Role), default=Role.user)
    images = relationship("Image", backref="users")
    # ratings = relationship("Rating", backref="user")
    avatar = Column(String(255), nullable=True)


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    public_id = Column(String(150))
    description = Column(String(150))
    created_at = Column("created_at", DateTime, default=func.now())
    updated_at = Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    user_id = Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None)
    tags = relationship("Tag", secondary=image_m2m_tag, back_populates="images")
    # transformed_link = relationship("TransformedImageLink", back_populates="image")
    comments = relationship("Comment", backref="images")
    qr_url = Column(String(255), nullable=True)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(13), nullable=False, unique=True)
    images = relationship("Image", secondary=image_m2m_tag, back_populates="tags")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment = Column(String(255), nullable=False)
    user_id = Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None)
    image_id = Column("image_id", ForeignKey("images.id", ondelete="CASCADE"), default=None)
    created_at = Column("created_at", DateTime, default=func.now())
    updated_at = Column("updated_at", DateTime, default=func.now(), onupdate=func.now())


# class Rating(Base):
#     __tablename__ = "ratings"
#     id = Column(Integer, primary_key=True)
#     rate = Column(Integer, default=0)
#     user_id = Column("user_id", ForeignKey("users.id", ondelete="CASCADE"))
#     image_id = Column("image_id", ForeignKey("images.id", ondelete="CASCADE"))
