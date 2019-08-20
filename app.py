from flask import Flask, redirect, request, jsonify, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
from flask_cors import CORS

import os
import math

from models import db, Document

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config["SECRET_KEY"] = "so secret that i dont even know what my secret key is"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

CORS(app)
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newdoc", methods=["POST"])
def new_doc():
    data = request.get_json()
    new_doc = Document(title="", body="", updated_at=data["new_datetime"], created_at=data["new_datetime"])
    db.session.add(new_doc)
    db.session.commit()

    new_doc.title = f"New Document({new_doc.id})"
    db.session.commit()

    return jsonify({"success": True, "doc_id": new_doc.id})

@app.route("/edit/<int:id>", methods=["PUT"])
def edit_doc(id):
    document = Document.query.filter_by(id=id).first()
    if document:
        data = request.get_json()
        document.title = data["title"]
        document.body = data["body"]
        document.updated_at = data["new_datetime"]
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route("/getdoc/<int:page_num>", methods=["GET"])
def get_doc(page_num):
    all_documents = len(Document.query.all())
    total_pages = math.ceil(all_documents/10)
    documents = Document.query.order_by(Document.updated_at.desc()).paginate(per_page=10, page=page_num, error_out=True).items
    document_array = []
    if documents:
        for document in documents:
            sending = {
                'id': document.id,
                'title': document.title,
                'body': document.body,
                'created_at': document.created_at,
                'updated_at': document.updated_at,
                # 'is_deleted': document.is_deleted
            }
            document_array.append(sending)
        return jsonify(total_pages=total_pages, results=document_array)
    else:
        return jsonify(results=document_array)

@app.route("/getalldoc", methods=["GET"])
def get_all_doc():
    documents = Document.query.order_by(Document.updated_at.desc()).all()
    document_array = []
    if documents:
        for document in documents:
            sending = {
                'id': document.id,
                'title': document.title,
                'body': document.body,
                'created_at': document.created_at,
                'updated_at': document.updated_at,
                # 'is_deleted': document.is_deleted
            }
            document_array.append(sending)
        return jsonify(results=document_array)
    else:
        return jsonify(results=document_array)

@app.route("/deldoc/<int:id>")
def del_doc(id):
    document = Document.query.filter_by(id=id).first()
    if document:
        db.session.delete(document)
        db.session.commit()
        return jsonify({ 'success': True })
    else:
        return jsonify({ 'success': False })

@app.route("/search/<text>", methods=["GET"])
def search_doc(text):
    search_text = f"%{text}%"
    documents = Document.query.filter(or_(Document.title.ilike(search_text), Document.body.ilike(search_text))).all()

    document_array = []

    if documents:
        for document in documents:
            sending = {
                'id': document.id,
                'title': document.title,
                'body': document.body,
                'created_at': document.created_at,
                'updated_at': document.updated_at,
                # 'is_deleted': document.is_deleted
            }
            document_array.append(sending)

        return jsonify(results=document_array)
    else:
        return jsonify(results=document_array)

if __name__ == '__main__':
    app.run()