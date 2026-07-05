from __future__ import annotations

from pathlib import Path

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    delete,
    event,
    func,
    insert,
    select,
    update,
)

metadata = MetaData()

student = Table(
    "student",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("full_name", String, nullable=False, unique=True),
)

subject = Table(
    "subject",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False, unique=True),
)

lesson = Table(
    "lesson",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "student_id",
        ForeignKey("student.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "subject_id",
        ForeignKey("subject.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("scheduled_on", String, nullable=False),
    Column("duration_minutes", Integer, nullable=False),
    CheckConstraint(
        "duration_minutes > 0", name="ck_lesson_duration_positive"
    ),
)


def reset_database_file(db_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()


def run_demo() -> None:
    db_path = Path(__file__).with_name("tuition_core.db")
    reset_database_file(db_path)

    engine = create_engine(f"sqlite+pysqlite:///{db_path}", future=True)

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record) -> None:  # type: ignore[no-untyped-def]
        del connection_record
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    metadata.create_all(engine)

    with engine.begin() as conn:
        conn.execute(
            insert(student),
            [
                {"full_name": "Alice Johnson"},
                {"full_name": "Bob Smith"},
                {"full_name": "Cara Lee"},
            ],
        )
        conn.execute(
            insert(subject),
            [
                {"title": "Mathematics"},
                {"title": "Physics"},
                {"title": "History"},
            ],
        )

        student_ids = {
            row["full_name"]: row["id"]
            for row in conn.execute(
                select(student.c.full_name, student.c.id)
            ).mappings()
        }
        subject_ids = {
            row["title"]: row["id"]
            for row in conn.execute(
                select(subject.c.title, subject.c.id)
            ).mappings()
        }

        conn.execute(
            insert(lesson),
            [
                {
                    "student_id": student_ids["Alice Johnson"],
                    "subject_id": subject_ids["Mathematics"],
                    "scheduled_on": "2026-03-24",
                    "duration_minutes": 60,
                },
                {
                    "student_id": student_ids["Bob Smith"],
                    "subject_id": subject_ids["Physics"],
                    "scheduled_on": "2026-03-24",
                    "duration_minutes": 45,
                },
                {
                    "student_id": student_ids["Cara Lee"],
                    "subject_id": subject_ids["History"],
                    "scheduled_on": "2026-03-25",
                    "duration_minutes": 50,
                },
            ],
        )

        conn.execute(
            update(student)
            .where(student.c.full_name == "Bob Smith")
            .values(full_name="Robert Smith")
        )
        conn.execute(
            update(lesson)
            .where(lesson.c.scheduled_on == "2026-03-24")
            .values(duration_minutes=lesson.c.duration_minutes + 15)
        )

        conn.execute(delete(lesson).where(lesson.c.duration_minutes >= 70))
        conn.execute(delete(subject).where(subject.c.title == "History"))

        print("\nLessons with student and subject:")
        lessons_stmt = (
            select(
                lesson.c.id,
                student.c.full_name,
                subject.c.title,
                lesson.c.scheduled_on,
                lesson.c.duration_minutes,
            )
            .join(student, student.c.id == lesson.c.student_id)
            .join(subject, subject.c.id == lesson.c.subject_id)
            .order_by(lesson.c.scheduled_on, lesson.c.id)
        )
        for row in conn.execute(lessons_stmt):
            print(tuple(row))

        print("\nLesson count by student:")
        count_stmt = (
            select(
                student.c.full_name,
                func.count(lesson.c.id).label("lesson_count"),
            )
            .select_from(
                student.outerjoin(lesson, lesson.c.student_id == student.c.id)
            )
            .group_by(student.c.id, student.c.full_name)
            .order_by(student.c.full_name)
        )
        for row in conn.execute(count_stmt):
            print(tuple(row))

        print("\nSubjects with no lessons:")
        empty_subjects_stmt = (
            select(subject.c.title)
            .select_from(
                subject.outerjoin(lesson, lesson.c.subject_id == subject.c.id)
            )
            .where(lesson.c.id.is_(None))
            .order_by(subject.c.title)
        )
        for row in conn.execute(empty_subjects_stmt):
            print(tuple(row))

    print(f"\nSQLite database created at: {db_path}")


if __name__ == "__main__":
    run_demo()
