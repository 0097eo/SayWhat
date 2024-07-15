# app.py
from flask import request, jsonify, make_response, session
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import app, db, api
from models import User, Post, Comment
from datetime import timedelta

class Signup(Resource):
    def post(self):
        data = request.get_json()
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.password_hash = data['password']
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 201)

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(days=4)
            )
            return {
                'access_token': access_token,
                'user_id': user.id,
                'username': user.username
            }, 200
        else:
            return {'message': 'Invalid username or password'}, 401

class Users(Resource):
    def get(self):
        users = User.query.all()
        return make_response(jsonify([{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'post_count': len(user.posts),
            'comment_count': len(user.comments)
        } for user in users]), 200)

class UserById(Resource):
    @jwt_required()
    def get(self, id):
        user = User.query.get(id)
        if user:
            return make_response(jsonify({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'posts': [{
                    'id': post.id,
                    'title': post.title,
                    'created_at': post.created_at
                } for post in user.posts],
                'comments': [{
                    'id': comment.id,
                    'content': comment.content,
                    'created_at': comment.created_at,
                    'post_id': comment.post_id
                } for comment in user.comments]
            }), 200)
        return {'error': 'User not found'}, 404

class Posts(Resource):
    def get(self):
        posts = Post.query.all()
        return make_response(jsonify([{
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'author': {
                'id': post.author.id,
                'username': post.author.username
            },
            'comment_count': len(post.comments)
        } for post in posts]), 200)

    @jwt_required()
    def post(self):
        data = request.get_json()
        claims = get_jwt_identity()
        user_id = claims['id']
        new_post = Post(
            title=data['title'],
            content=data['content'],
            author_id=user_id
        )
        db.session.add(new_post)
        db.session.commit()
        return make_response(jsonify({
            'id': new_post.id,
            'title': new_post.title,
            'content': new_post.content,
            'created_at': new_post.created_at,
            'author_id': new_post.author_id
        }), 201)

class PostById(Resource):
    def get(self, id):
        post = Post.query.get(id)
        if post:
            return make_response(jsonify({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'author': {
                    'id': post.author.id,
                    'username': post.author.username
                },
                'comments': [{
                    'id': comment.id,
                    'content': comment.content,
                    'created_at': comment.created_at,
                    'author': {
                        'id': comment.author.id,
                        'username': comment.author.username
                    }
                } for comment in post.comments]
            }), 200)
        return {'error': 'Post not found'}, 404

    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        author_id = claims
        post = Post.query.get(id)
        if not post:
            return {'error': 'Post not found'}, 404
        if post.author_id != author_id:
            return {'error': 'Unauthorized'}, 403
    
        data = request.get_json()
    
        for attr in ['title', 'content']:
            if attr in data:
                setattr(post, attr, data[attr])    
        db.session.commit()
        return make_response(jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'updated_at': post.updated_at
        }), 200)

    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        author_id = claims['id']
        post = Post.query.get(id)
        if not post:
            return {'error': 'Post not found'}, 404
        if post.author_id != author_id:
            return {'error': 'Unauthorized'}, 403
        db.session.delete(post)
        db.session.commit()
        return '', 204

class Comments(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()  # This directly returns the user ID
        new_comment = Comment(
            content=data['content'],
            author_id=user_id,
            post_id=data['post_id']
        )
        db.session.add(new_comment)
        db.session.commit()
        return make_response(jsonify({
            'id': new_comment.id,
            'content': new_comment.content,
            'created_at': new_comment.created_at,
            'author_id': new_comment.author_id,
            'post_id': new_comment.post_id
        }), 201)

class CommentById(Resource):
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        user_id = claims['id']
        comment = Comment.query.get(id)
        if not comment:
            return {'error': 'Comment not found'}, 404
        if comment.author_id != user_id:
            return {'error': 'Unauthorized'}, 403
        db.session.delete(comment)
        db.session.commit()
        return '', 204
    
class CommentsByPost(Resource):
    def get(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return {'error': 'Post not found'}, 404
        
        comments = Comment.query.filter_by(post_id=post_id).all()
        comment_count = len(comments)
        
        comments_data = [{
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at,
            'author': {
                'id': comment.author.id,
                'username': comment.author.username
            }
        } for comment in comments]
        
        return make_response(jsonify({
            'post_id': post_id,
            'comment_count': comment_count,
            'comments': comments_data
        }), 200)

# Add resources to API
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<int:id>')
api.add_resource(Posts, '/posts')
api.add_resource(PostById, '/posts/<int:id>')
api.add_resource(Comments, '/comments')
api.add_resource(CommentById, '/comments/<int:id>')
api.add_resource(CommentsByPost, '/posts/<int:post_id>/comments')

if __name__ == '__main__':
    app.run(port=5555, debug=True)