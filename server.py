from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
import os


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/schedulord.db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath('.'), 'uploads')
db = SQLAlchemy(app)


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    interval = db.Column(db.Integer)
    script_name = db.Column(db.Text)
    next_runtime = db.Column(db.DateTime)


# App routes
@app.route('/jobs')
def index():
    all_jobs = Job.query.all()
    all_jobs = { x.name: {'id': x.id, 'name': x.name, 'interval': x.interval} for x in all_jobs}
    return jsonify(jobs=all_jobs)


@app.route('/jobs/create', methods=['POST'])
def create():
    file = request.files['file']
    json_data = request.form
    filename = secure_filename(file.filename)
    script_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(script_path)
    script_name = filename.rstrip('.py')
    
    # creating a job
    job = Job(name=json_data['name'],
            interval=json_data['interval'],
            next_runtime=None,
            script_name=script_name
            )
    db.session.add(job)
    db.session.commit()
    return "{0} has been uploaded".format(filename)


@app.route('/jobs/<id>', methods=['GET'])
def read(id):
    return "read method"


@app.route('/jobs/<id>', methods=['DELETE'])
def delete(id):
    job = Job.query.get(id)
    job_name = job.name
    job.query.delete()
    db.session.commit()
    return "job {} has been deleted".format(job_name)


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(debug=True)
