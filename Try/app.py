from flask import Flask, render_template
from data import article_creator

app = Flask(__name__)

articles = article_creator()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/articles')
def get_articles():
	return render_template('articles.html', articles=articles)

@app.route('/article/<string:id>/')
def get_article(id):
	return render_template('article.html', id=id)


if __name__ == "__main__":
	app.run(debug=True)
