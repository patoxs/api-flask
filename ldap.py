# coding=utf-8

from flask import Flask
from flask.ext.ldap import LDAP
app = Flask(__name__)
app.debug = True
app.config['LDAP_HOST'] = '10.14.1.4'
app.config['LDAP_PORT'] = '389'
app.config['LDAP_DOMAIN'] = 'INDAP\\'
#app.config['LDAP_AUTH_TEMPLATE'] = 'login.html'
#app.config['LDAP_PROFILE_KEY'] = 'employeeID'
app.config['LDAP_AUTH_VIEW'] = 'login'

ldap = LDAP(app)
app.secret_key = "welfhwdlhwdlfhwelfhwlehfwlehfelwehflwefwlehflwefhlwefhlewjfhwelfjhweflhweflhwel"
app.add_url_rule('/login', 'login', ldap.login, methods=['GET', 'POST'])

@app.route('/')
@ldap.login_required
def index():
	return "auteticado con ldap"
	pass


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     pass

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")