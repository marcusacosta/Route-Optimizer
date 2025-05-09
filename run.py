# Entry point for Flask app
from app import create_app
import logging

app = create_app()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

if __name__ == "__main__":
    app.run(debug=True)
