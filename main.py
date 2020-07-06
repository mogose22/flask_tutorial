from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_flask_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        print("Create article.\ntitle: {}, intro: {}, text: {}".format(title, intro, text))
        article = Article(title=title, intro=intro, text=text)
        print("Create Article object is OK!")
        try:
            db.session.add(article)
            print("db.session.add is ok!")
            db.session.commit()
            print('db.session.commit is ok!')
            return redirect('/')
        except Exception as e:
            return "При добавлении статьи произошла ошибка: %e " %e
    else:
        return render_template("create-article.html")

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
