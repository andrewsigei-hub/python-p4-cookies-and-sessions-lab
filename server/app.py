#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate

from models import db, Article

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear', methods=['DELETE'])
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    # Initialize page_views to 0 on first request
    session['page_views'] = session.get('page_views', 0)
    
    # Increment page views for this request
    session['page_views'] += 1
    
    # Check if within the 3-article limit
    if session['page_views'] <= 3:
        # Fetch the article from database
        article = Article.query.filter(Article.id == id).first()
        
        # Handle case where article doesn't exist
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        # Return article data as JSON
        return jsonify(article.to_dict()), 200
    else:
        # Return error message with 401 status
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)