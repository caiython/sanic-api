from sanic import Sanic
import os
import aiosqlite


async def run_migrations(migrations_path='app/migrations'):

    db_path = Sanic.get_app().config.DB_PATH

    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS migration_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_name TEXT NOT NULL UNIQUE,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        await db.commit()

        scripts_folder_path = os.path.join(migrations_path, 'scripts')
        for migration in sorted(os.listdir(scripts_folder_path)):
            if migration.endswith(".sql"):
                script_path = os.path.join(scripts_folder_path, migration)

                async with db.execute('SELECT COUNT(1) FROM migration_history WHERE migration_name = ?', (migration,)) as cursor:
                    already_applied = await cursor.fetchone()
                    
                if already_applied[0] == 0:
                    with open(script_path, 'r') as file:
                        sql_script = file.read()
                        await db.executescript(sql_script)

                    await db.execute('''
                        INSERT INTO migration_history (migration_name) VALUES (?);
                    ''', (migration,))
                    await db.commit()