import os
import asyncpg, dotenv

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        try:
            # since we have no Authentication, we can just use the URL
            self.pool = await asyncpg.create_pool(DATABASE_URL, ssl=True, min_size=1, max_size=15)

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

    async def set_log(self, keystroke_count: str, click_count: str, ratio: str):
        try:
            # gets the database connection from pool
            async with self.pool.acquire() as conn:
                # inserting/updating LOG-DATA
                await conn.execute("""
                    -- inserts a new line in the table
                    INSERT INTO LOG (keystroke_count, click_count, ratio)
                    -- $1, $2 & $3 are asyncpg placeholders
                    VALUES ($1, $2, $3)
                    -- conflict occurs when the variable_name already exists
                    -- if the variable_name already exists, it updates the variable_value
                    ON CONFLICT (date) DO UPDATE
                    SET keystroke_count = $1,
                    click_count = $2,
                    ratio = $3
                """,
                str(keystroke_count),
                str(click_count),
                str(ratio)
                )
                print("✅ TABLE set successfully!")
        except Exception as error:
            print(f"❌ Error setting/updating TABLE: {error}")
            
    async def get_last_log(self):
        try:
            # gets the database connection from pool
            async with self.pool.acquire() as conn:
                result = await conn.fetchrow("""
                    -- gets the last log from the table
                    SELECT *
                    FROM LOG
                    ORDER BY date DESC
                    LIMIT 1
                """)
                # returning the last log
                return result
        except Exception as error:
            print(f"Error at fetching last log: {error}")
            return None

db = Database()