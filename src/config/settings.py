

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


DATABASE = {
	"default": {
		"engine": "src.seedwork.infrastructure.database.SQLiteManager",
		"path": "database/db.sqlite3"
	}
}


TRANSLATIONS = {
	"es": {
		"path": "fmotor/ui/translations/es.csv"
	}
}

LANGUAGE = "es"

