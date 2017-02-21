from flask import Flask, render_template, redirect, session, url_for, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'dbms'
app.config['MONGO_URI'] = 'mongodb://sanchit:sanchit@ds145369.mlab.com:45369/dbms'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('search.html')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['pass'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['pass']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
	data = mongo.db.records
	output = []
	if len(request.form['student_name']) > 0:
		if request.form['student_name'] == "all":
			for x in range(1,data.count()+1):
				student = data.find_one({'sno' :x})
				temp = {'sno' : student['sno'], 'name' : student['name'], 'age' : student['age'], 'CGPA' : student['CGPA']}
				output.append(temp)
		else:
			student = data.find_one({'name' : request.form['student_name']})
			if student:
				temp = {'sno' : student['sno'], 'name' : student['name'], 'age' : student['age'], 'CGPA' : student['CGPA']}
				output.append(temp)

	elif request.form['lower_bound'] is not None and request.form['upper_bound'] is not None:
		for x in range(1,data.count()+1):
			student = data.find_one({'sno':x})
			if student['CGPA']>=int(request.form['lower_bound']) and student['CGPA']<=int(request.form['upper_bound']):
				temp = {'sno' : student['sno'], 'name' : student['name'], 'age' : student['age'], 'CGPA' : student['CGPA']}
				output.append(temp)
		
	return render_template('search.html', output = output)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)	 