from flask import Flask
from flask_cors import CORS
from routes.missions import missions_bp
from routes.fleet import fleet_bp
from routes.reports import reports_bp

app = Flask(__name__)
CORS(app)  

app.register_blueprint(missions_bp)
app.register_blueprint(fleet_bp)
app.register_blueprint(reports_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
