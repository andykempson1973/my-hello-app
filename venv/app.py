from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # This will look for 'index.html' in a 'templates' folder
    return render_template("index.html", name="Developer")

@app.route("/hello/<name>")
def hello_name(name):
    # Pass the name variable to the template
    return render_template("index.html", name=name.title())

if __name__ == "__main__":
    # Running the app locally
    app.run(debug=True)