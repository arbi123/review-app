from app import create_app

app = create_app()

if __name__ == "__main__":
    import logging

    logging.getLogger(__name__).info(
        "Starting TasteMap on http://127.0.0.1:5000 — press Ctrl+C to stop."
    )
    app.run(debug=True)
