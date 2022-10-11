from api import create_app

if __name__ == "__main__":
    # Create app.
    app = create_app()

    # Run app. For production use another web server.
    # Set debug and use_reloader parameters as False.
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=True)
