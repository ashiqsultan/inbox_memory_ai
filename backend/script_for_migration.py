import os
import sys
from pathlib import Path
from yoyo import read_migrations, get_backend
from typing import Optional


def run_migrations(database_url: Optional[str] = None) -> None:
    """
    Run database migrations using yoyo-migrations.

    Args:
        database_url: Optional database URL. If not provided, will use environment variable.
    """
    if database_url is None:
        database_url = os.getenv("DATABASE_URL", "")

    # Get the absolute path to the migrations directory
    migrations_path = Path(__file__).parent / "migrations"

    try:
        backend = get_backend(database_url)
        migrations = read_migrations(str(migrations_path))

        with backend.lock():
            # Apply any outstanding migrations
            backend.apply_migrations(backend.to_apply(migrations))
            print("✅ Migrations completed successfully")

    except Exception as e:
        print(f"❌ Error running migrations: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Allow passing database URL as command line argument
    db_url = sys.argv[1] if len(sys.argv) > 1 else None
    run_migrations(db_url)
