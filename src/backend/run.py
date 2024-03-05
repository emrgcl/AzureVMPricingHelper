from app import create_app

app = create_app('instance.config.Config')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
