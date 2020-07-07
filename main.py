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
            return redirect('/posts')
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
    
@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    print("Зашли в post_detail. post_id={}".format(post_id))
    article = Article.query.get(post_id)
    print("Объект Article создан. Дальше возврат шаблона.")
    return render_template('post-detail.html', article=article)
    
@app.route('/posts/<int:post_id>/delete')
def post_delete(post_id):
    print("Зашли в post_delete. post_id={}".format(post_id))
    article = Article.query.get_or_404(post_id)
    try:
        print("пытаемся удалить запись {}".format(post_id))
        db.session.delete(article)
        print("пытаемся закоммитить изменения")
        db.session.commit()
        print("успешно! редирект на /posts")
        return redirect('/posts')
    except Exception as e:
        return "При удалении статьи произошла ошибка {}".format(e)
 
 
@app.route('/posts/<int:post_id>/update', methods=['POST', 'GET'])
def post_update(post_id):
    article = Article.query.get(post_id)
    
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        print("update article.\ntitle: {}, intro: {}".format(article.title, article.intro))
        try:
            db.session.commit()
            print('db.session.commit is ok!')
            return redirect('/posts')
        except Exception as e:
            return "При редактировании статьи произошла ошибка: {} ".format(e)
    else:
        return render_template("post-update.html", article=article)


    
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
