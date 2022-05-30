########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, flash,request,redirect
from flask_login import login_required, current_user
from __init__ import create_app, db
from constants import file_constants as cnst
from processing import resume_matcher
from utils import file_utils
import os


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','docx'])

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('resume_loader.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@main.route('/failure')
def failure():
   return 'No files were selected'

@main.route('/success/<name>')
def success(name):
   return 'Files %s has been selected' %name

@main.route('/resume_results', methods=['POST', 'GET'])
def check_for_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'reqFile' not in request.files:
           flash('Requirements document can not be empty')
           return redirect(request.url)
        if 'resume_files' not in request.files:
           flash('Select at least one resume File to proceed further')
           return redirect(request.url)
        file = request.files['reqFile']
        if file.filename == '':
           flash('Requirement document has not been selected')
           return redirect(request.url)
        resume_files = request.files.getlist("resume_files")
        if len(resume_files) == 0:
            flash('Select atleast one resume file to proceed further')
            return redirect(request.url)
        if ((file and allowed_file(file.filename)) and (len(resume_files) > 0)):
           #filename = secure_filename(file.filename)
           abs_paths = []
           filename = file.filename
           
           req_document = app.config['UPLOAD_FOLDER']+'/'+filename
           
            

           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

           for resumefile in resume_files:
               filename = resumefile.filename
               
               abs_paths.append(app.config['UPLOAD_FOLDER']+ '/' + filename)
               resumefile.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))


           result = resume_matcher.process_files(req_document,abs_paths)
           for file_path in abs_paths:
               file_utils.delete_file(file_path)

           return render_template("resume_results.html", result=result)
        else:
           flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
           return redirect(request.url)

app = create_app() # we initialize our flask app using the __init__.py function

if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    # EDIT: Added host and port parameters so that the Docker can access the appropriate ports to connect to the app
    app.run(debug=True, host='0.0.0.0',port=os.environ.get("PORT", 5000)) # run the flask app on debug mode
