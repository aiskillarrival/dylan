from __future__ import annotations

from pathlib import Path

from sqlalchemy import ForeignKey, String, create_engine, event, func, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String, unique=True)
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )


class Lesson(Base):
    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="CASCADE")
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subject.id", ondelete="CASCADE")
    )
    scheduled_on: Mapped[str]
    duration_minutes: Mapped[int]

    student: Mapped[Student] = relationship(back_populates="lessons")
    subject: Mapped[Subject] = relationship(back_populates="lessons")


def reset_database_file(db_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()


def run_demo() -> None:
    db_path = Path(__file__).with_name("tuition_orm.db")
    reset_database_file(db_path)

    engine = create_engine(f"sqlite+pysqlite:///{db_path}", future=True)

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record) -> None:  # type: ignore[no-untyped-def]
        del connection_record
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        alice = Student(full_name="Alice Johnson")
        bob = Student(full_name="Bob Smith")
        cara = Student(full_name="Cara Lee")

        maths = Subject(title="Mathematics")
        physics = Subject(title="Physics")
        history = Subject(title="History")

        session.add_all([alice, bob, cara, maths, physics, history])
        session.flush()

        session.add_all(
            [
                Lesson(
                    student=alice,
                    subject=maths,
                    scheduled_on="2026-03-24",
                    duration_minutes=60,
                ),
                Lesson(
                    student=bob,
                    subject=physics,
                    scheduled_on="2026-03-24",
                    duration_minutes=45,
                ),
                Lesson(
                    student=cara,
                    subject=history,
                    scheduled_on="2026-03-25",
                    duration_minutes=50,
                ),
            ]
        )

        bob.full_name = "Robert Smith"

        for lesson_obj in session.scalars(
            select(Lesson).where(Lesson.scheduled_on == "2026-03-24")
        ):
            lesson_obj.duration_minutes += 15

        session.query(Lesson).filter(Lesson.duration_minutes >= 70).delete(
            synchronize_session=False
        )

        history_subject = session.scalar(
            select(Subject).where(Subject.title == "History")
        )
        if history_subject is not None:
            session.delete(history_subject)

        session.commit()

    with Session(engine) as session:
        print("\nLessons with student and subject:")
        lessons_stmt = (
            select(
                Lesson.id,
                Student.full_name,
                Subject.title,
                Lesson.scheduled_on,
                Lesson.duration_minutes,
            )
            .join(Lesson.student)
            .join(Lesson.subject)
            .order_by(Lesson.scheduled_on, Lesson.id)
        )
        for row in session.execute(lessons_stmt):
            print(tuple(row))

        print("\nLesson count by student:")
        count_stmt = (
            select(
                Student.full_name, func.count(Lesson.id).label("lesson_count")
            )
            .outerjoin(Student.lessons)
            .group_by(Student.id, Student.full_name)
            .order_by(Student.full_name)
        )
        for row in session.execute(count_stmt):
            print(tuple(row))

        print("\nSubjects with no lessons:")
        empty_subjects_stmt = (
            select(Subject.title)
            .outerjoin(Subject.lessons)
            .where(Lesson.id.is_(None))
            .order_by(Subject.title)
        )
        for row in session.execute(empty_subjects_stmt):
            print(tuple(row))

    print(f"\nSQLite database created at: {db_path}")


if __name__ == "__main__":
    run_demo()
