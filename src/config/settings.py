

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


DATABASE = {
	"default": {
		"engine": "src.seedwork.infrastructure.database.SQLiteManager",
		"path": BASE_DIR / "database/db.sqlite3"
	}
}


TRANSLATIONS = {
	"es": {
		"path": BASE_DIR / "fmotor/ui/translations/es.csv"
	}
}

LANGUAGE = "es"

