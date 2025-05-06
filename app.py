from flask import Flask, render_template
from auth import auth
from upload import upload

app = Flask (__name__)
app.secret_key = '3d9f728e4c2b3f6f8e5a1c7a8b9d2f3e4c5a6b7d8e9f0a1b2c3d4e5f6a7b8c9d'

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(upload, url_prefix='/upload')

# Route till startsidan
@app.route('/')
def index():
    return render_template('index.html')

# Route till login sidan
@app.route('/login')
def login():
    return render_template('login.html')

# Route till profil sidan
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Route till portfoliosidan
@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

# Route till sida för att ladda upp inlägg
@app.route('/upload')
def upload():
    return render_template('upload.html')

# Route till felhantering 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')



# Säkerställer att fel meddelas under testning
if __name__ == '__main__':
    app.run(debug=True)