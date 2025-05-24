import enum
from datetime import date
from typing import Any, Optional
import validators
from slugify import slugify
from sqlalchemy import Boolean, Date, Enum, event, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, validates
from app.extensions import db


class WorkExperience(db.Model):  # type: ignore[name-defined]
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    company: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(25))
    zipcode: Mapped[str] = mapped_column(String(16))
    description: Mapped[str] = mapped_column(Text)
    start_date: Mapped[date] = mapped_column(Date, index=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date)

    @property
    def is_current(self) -> bool:
        return self.end_date is None
    
    def __repr__(self) -> str:
        return f'<WorkExperience {self.title}>'


class ProjectStatus(enum.Enum):
    COMPLETE = 'complete'
    IN_PROGRESS = 'in_progress'


class Project(db.Model):  # type: ignore[name-defined]
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(150), unique=True)
    summary: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        Enum(ProjectStatus),
        default=ProjectStatus.IN_PROGRESS
    )
    github_url: Mapped[Optional[str]] = mapped_column(String(2048))
    begin_date: Mapped[date] = mapped_column(Date, index=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    @validates('github_url')
    def validate_github_url(self, key: Any, value: str) -> str:
        if not validators.url(value):
            raise ValueError(f'Invalid URL: {value}')
        return value
    
    @property
    def date_str(self) -> str:
        dt = self.begin_date.strftime('%b %Y')
        if self.status == ProjectStatus.IN_PROGRESS:
            dt += ' \u2013 PRESENT'
        else:
            if self.end_date is not None:
                dt += f' \u2013 {self.end_date.strftime("%b %Y")}'

        return dt
    
    @staticmethod
    def generate_slug(target: 'Project', value: str, oldvalue: str, initiator: Any) -> None:
        if value and (not target.slug or value != oldvalue):
            base_slug = slugify(value)
            similar_slug_count = db.session.query(Project).filter(
                Project.id != target.id,
                Project.slug.like(base_slug + '%')
            ).count()
            if similar_slug_count > 0:
                target.slug = f'{base_slug}-{similar_slug_count + 1}'
            else:
                target.slug = base_slug

    def __repr__(self) -> str:
        return f'<Project {self.name}>'

event.listen(Project.name, 'set', Project.generate_slug, retval=False)
