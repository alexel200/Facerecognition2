from src addimport create_app

app = create_app()
print("folder", app.config['BASE_PATH'])
if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )