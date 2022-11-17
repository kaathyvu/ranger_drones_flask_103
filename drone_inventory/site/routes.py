from flask import Blueprint, render_template
from flask_login import login_required

site = Blueprint('site', __name__, template_folder='site_templates')
"""
Note that in the above code, some arguments are specified when creating a blueprint object
- 'site' = Blueprint name as a string, which is used by Flask's routing mechanism
- __name__ = Blueprint's import name, which Flask uses to locate the Blueprint's resources
- template_folder = tells Flask where to find the HTML to render

"""

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
    