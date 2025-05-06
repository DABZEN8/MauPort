from flask import Blueprint, render_template

upload = Blueprint('upload', __name__)

@upload.route('/upload')
def upload_file():
    return render_template('upload.html')

#if __name__ == '__main__':
    upload.run(debug=True)
    
    
    