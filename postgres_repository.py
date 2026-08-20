import psycopg


class PostgresTaskRepository:

    def __init__(self, database_url):
        self.database_url = database_url

    def get_tasks(self):
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, done FROM tasks ORDER BY id"
                )
                rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "done": bool(row[2])
            }
            for row in rows
        ]

    def get_task(self, task_id):
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks
                    WHERE id = %s
                    """,
                    (task_id,)
                )

                row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }

    def create_task(self, title):
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (%s, %s)
                    RETURNING id, title, done
                    """,
                    (title, False)
                )

                row = cursor.fetchone()

        return {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }

    def update_task(self, task_id, title, done):
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s, done = %s
                    WHERE id = %s
                    RETURNING id, title, done
                    """,
                    (title, done, task_id)
                )

                row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }

    def delete_task(self, task_id):
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM tasks
                    WHERE id = %s
                    RETURNING id
                    """,
                    (task_id,)
                )

                row = cursor.fetchone()

        return row is not None