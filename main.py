from flask import Flask
from app.business_area import BusinessAreaController

app = Flask(__name__)
app.debug = True
app.config['SERVER_NAME'] = '127.0.0.1:5000'

app.register_blueprint(BusinessAreaController)

@app.route('/anther/api')
def home():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)