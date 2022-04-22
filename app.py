from unicodedata import name
from flask import Flask, redirect,render_template, request, url_for
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/terms.html")
def terms_html():
    return render_template("terms.html")
  
# Route for handling the login page logic
#@app.route('/login.html', methods=['GET', 'POST'])
#def login_html():
    #error = None
    #if request.method == 'POST':
        #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            #error = 'Invalid. Please try again.'
        #else:
            #return redirect(url_for('login'))
    #return render_template('resumeparser.html', error=error)


@app.route("/login.html")
def logintry_html():
    return render_template ("login.html")


@app.route("/resumeparser.html",methods=['POST'])
def resumeparser_html():
    return render_template("resumeparser.html") 

@app.route("/try.html")
def try_html():
    return render_template ("try.html")     

if __name__== '__main__':
    app.run(debug=True)  
    