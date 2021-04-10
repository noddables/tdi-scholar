'''procedure: start app and make sure app is running on correct port'''
# import os
# from flask import Flask
# app = Flask(__name__)
# @app.route("/")
# def hello():
#     return "Hello world!"
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)
from flask import Flask
from flask import render_template
# from flask import request
# from flask import redirect
CharlieTdiMilestoneProject = Flask(__name__)
@CharlieTdiMilestoneProject.route('/')
def index():
    return render_template('CharlieTdiMilestoneProject.html')
@CharlieTdiMilestoneProject.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    CharlieTdiMilestoneProject.run(port=33507)