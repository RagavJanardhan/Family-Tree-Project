from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Flask will automatically look in the 'templates' folder

@app.route('/family_tree.json')
def get_family_tree():
    return send_from_directory(os.getcwd(), 'family_tree.json')

if __name__ == '__main__':
    app.run(debug=True)
