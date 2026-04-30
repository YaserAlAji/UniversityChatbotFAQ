import os
import sys

# Ensure the backend module can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import app, db_path, init_db
import os

if __name__ == '__main__':
    # Ensure data directory exists
    data_dir = os.path.dirname(db_path)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Initialize DB if not exists
    if not os.path.exists(db_path):
        init_db()

    app.run(debug=True)
