import asyncpg
import config
import datetime

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        try:
            # since we have no Authentication, we can just use the URL
            self.pool = await asyncpg.create_pool(config.DATABASE_URL, ssl=True)

            # gets the database connection from pool
            async with self.pool.acquire() as conn:
                await conn.execute("CREATE SCHEMA IF NOT EXISTS public")
                await conn.execute("SET search_path TO public")

            print("✅Connected to the database.")

            await self.create_tables()
        except Exception as error:
            print(f"❌Failed to connect to the database: {error}")

    async def create_tables(self):
        try:
            # gets the database connection from pool
            async with self.pool.acquire() as conn:
                # creating a SQL table for logging
                await conn.execute(
                    """
                    -- creating a table called 'LOG' if not exists
                    CREATE TABLE IF NOT EXISTS LOG (
                        date DATE DEFAULT (CURRENT_DATE AT TIME ZONE 'Asia/Dhaka'),
                        keystroke_count TEXT,
                        click_count TEXT,
                        ratio TEXT,
                        -- ensures that the date is unique
                        PRIMARY KEY (date)
                    );
                """
                )
                print("✅ Variables table ready!")
        except Exception as error:
            print(f"❌ Error creating tables: {error}")

    async def set_log(self, date: str, keystroke_count: str, click_count: str, ratio: str):
        try:
            # gets the database connection from pool
            async with self.pool.acquire() as conn:
                # inserting/updating LOG-DATA
                await conn.execute("""
                    -- inserts a new line in the table
                    INSERT INTO LOG (date, keystroke_count, click_count, ratio)
                    -- $1, $2, $3 & $4 are asyncpg placeholders
                    VALUES ($1, $2, $3, $4)
                """,
                datetime.datetime.strptime(date, "%Y-%m-%d").date(),
                str(keystroke_count),
                str(click_count),
                str(ratio)
                )
                print("✅ TABLE set successfully!")
        except Exception as error:
            print(f"❌ Error setting/updating TABLE: {error}")
            

db = Database()