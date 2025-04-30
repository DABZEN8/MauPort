from flask import Flask, render_template
from auth import auth

app = Flask (__name__)

app.register_blueprint(auth, url_prefix='/auth')

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

# Route till felhantering 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')




# Säkerställer att fel meddelas under testning
if __name__ == '__main__':
    app.run(debug=True)