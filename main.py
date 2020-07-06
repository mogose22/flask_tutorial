from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/users/<string:name>/<int:user_id>')
def users(name:str, user_id: int):
    return 'User page: {} {}'.format(name, user_id)

if __name__ == '__main__':
    app.run(debug=True)
