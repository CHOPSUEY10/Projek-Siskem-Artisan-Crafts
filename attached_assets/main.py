
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
# Use SQLite database - simple file-based database with no server required


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)