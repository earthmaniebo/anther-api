from flask import Flask
from app.business_area import BusinessAreaController
from app.business_domain import BusinessDomainController
from app.service_domain import ServiceDomainController

app = Flask(__name__)
app.debug = True

app.register_blueprint(BusinessAreaController)
app.register_blueprint(BusinessDomainController)
app.register_blueprint(ServiceDomainController)

@app.route('/anther/api')
def home():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001, threaded=True)
