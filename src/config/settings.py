

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


DATABASE = {
	"default": {
		"engine": "src.seedwork.infrastructure.database.SQLiteManager",
		"path": "config/database/db.sqlite3"
	}
}

