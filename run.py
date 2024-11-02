from app import create_app, db

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Initialiser la base de données."""
    db.create_all()
    print('Base de données initialisée.')

if __name__ == '__main__':
    app.run(debug=True) 