from bluelog import app


@app.route('/')
def index():
    return 'Hello From mogai'
