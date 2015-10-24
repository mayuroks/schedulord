from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/schedulord.db'
db = SQLAlchemy(app)


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    interval = db.Column(db.Integer)
    func = db.Column(db.LargeBinary)
    next_runtime = db.Column(db.DateTime)



manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Job, methods=['GET', 'POST', 'DELETE', 'PATCH'], url_prefix="/api", collection_name="jobs", allow_patch_many=True)

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run()
