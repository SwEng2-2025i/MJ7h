from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

service_d = Flask(__name__)
CORS(service_d)

service_d.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pdf.db'
service_d.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(service_d)

class Log_PDF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)


# Endpoint para guardar la tarea en la DB.
@service_d.route('/pdf/logs', methods=['POST'])
def create_log():
    # Endpoint para guardar la tarea en la DB.
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Datos inválidos'}), 400

    log = Log_PDF(title=data['title'])
    db.session.add(log)
    db.session.commit()
    return jsonify({'id': log.id, 'title': log.title}), 200

@service_d.route('/pdf/logs', methods=['GET'])
def get_logs():
    logs = Log_PDF.query.all()
    return jsonify([{'id': l.id, 'title': l.title} for l in logs]), 200

@service_d.route('/pdf/logs/getId', methods=['GET'])
def get_next_id():
    last_log = Log_PDF.query.order_by(Log_PDF.id.desc()).first()
    if last_log:
        result =  last_log.id + 1
    else:
        result = 1
    return jsonify({'id': result}), 200

if __name__ == '__main__':
    with service_d.app_context():
        db.create_all()
    service_d.run(port=5004)