#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, jsonify, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Blog, Comment, Channel, UserChannel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# Views go here!

class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.password == data['password']:  # Replace with proper password hashing
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token)
        return {'message': 'Invalid credentials'}, 401


class UserResource(Resource):    
    def post(self):
        data = request.get_json()
        
        username=data['username']
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400
        email=data['email'],
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, 400
        password = data['password']

        new_user = User(
            username=username,
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user), 201
    #updating user information after signing up
    @jwt_required()
    def patch(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        user = User.query.filter_by(id=current_user_id).first() 
        if user:
            if 'email' in data:
                user.email = data['email']
            if 'profile_pic' in data:
                user.profile_pic = data['profile_pic']
            if 'age' in data:
                user.age = data['age']
            if 'dob' in data:
                user.dob = data['dob']
            if 'phone_number' in data:
                user.phone_number = data['phone_number']
            db.session.commit()
            return jsonify(user.to_dict())
        return {'message': 'User not found'}, 404
    #deleting user
    @jwt_required()
    def delete(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}
        return {'message': 'User not found'}, 404

class BlogResource(Resource):
    #view all blogs or blogs in a particular channel
    #@jwt_required()
    def get(self, channel_id=None):
        if channel_id:
            blogs = Blog.query.filter_by(channel_id=channel_id).all()
            if blogs:
                return make_response(jsonify([blog.to_dict() for blog in blogs]), 200)
            return make_response({'message': 'Blog not found'}, 404)
        blogs = Blog.query.all()
        return make_response(jsonify([blog.to_dict() for blog in blogs]), 200)
    #add new blog
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        channel_id = data.get('channel_id')

        user_channel = UserChannel.query.filter_by(user_id=current_user_id, channel_id=channel_id).first()
        if not user_channel:
            return {'message': 'Unauthorized'}, 401
        
        new_blog = Blog(
            content=data['content'],
            topic=data['topic'],
            user_id=current_user_id,
            channel_id=channel_id
        )
        db.session.add(new_blog)
        db.session.commit()
        return jsonify(new_blog), 201
    
    def delete(self, blog_id):
        blog = Blog.query.get(blog_id)
        if blog:
            db.session.delete(blog)
            db.session.commit()
            return {'message': 'Blog deleted'}
        return {'message': 'Blog not found'}, 404

class CommentResource(Resource):
    #@jwt_required()
    def get(self, blog_id):
        comments = Comment.query.filter_by(blog_id=blog_id).all()
        return make_response([comment.to_dict() for comment in comments], 200)
    @jwt_required()
    def post(self, blog_id):
        current_user = get_jwt_identity()

        blog=Blog.query.get(blog_id)
        if not blog:
            return {'message': 'Blog not found'}, 404
        data = request.get_json()
        new_comment = Comment(
            message=data['message'],
            body=data['body'],
            user_id=current_user,
            blog_id=blog_id
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment), 201
    
    
    def delete(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return {'message': 'Comment deleted'}
        return {'message': 'Comment not found'}, 404

class ChannelResource(Resource):
    def get(self, channel_id=None):
        if channel_id:
            channel = Channel.query.get(channel_id)
            if channel:
                return jsonify(channel)
            return {'message': 'Channel not found'}, 404
        channels = Channel.query.all()
        return jsonify(channels)
    
    def post(self):
        data = request.get_json()
        new_channel = Channel(
            channel_name=data['channel_name'],
            creator_id=data['creator_id'],
            owner=data['owner']
        )
        db.session.add(new_channel)
        db.session.commit()
        return jsonify(new_channel), 201
    def delete(self, channel_id):
        channel = Channel.query.get(channel_id)
        if channel:
            db.session.delete(channel)
            db.session.commit()
            return {'message': 'Channel deleted'}
        return {'message': 'Channel not found'}, 404

class UserChannelResource(Resource):
    def get(self, user_channel_id=None):
        if user_channel_id:
            user_channel = UserChannel.query.get(user_channel_id)
            if user_channel:
                return jsonify(user_channel)
            return {'message': 'User-Channel not found'}, 404
        user_channels = UserChannel.query.all()
        return jsonify(user_channels)
    
    def post(self):
        data = request.get_json()
        new_user_channel = UserChannel(
            user_id=data['user_id'],
            channel_id=data['channel_id']
        )
        db.session.add(new_user_channel)
        db.session.commit()
        return jsonify(new_user_channel), 201
    
    def delete(self, user_channel_id):
        user_channel = UserChannel.query.get(user_channel_id)
        if user_channel:
            db.session.delete(user_channel)
            db.session.commit()
            return {'message': 'User-Channel deleted'}
        return {'message': 'User-Channel not found'}, 404

# Add resources to API
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(BlogResource, '/blogs', '/blogs/<int:blog_id>')
api.add_resource(CommentResource, '/comments', '/comments/<int:comment_id>')
api.add_resource(ChannelResource, '/channels', '/channels/<int:channel_id>')
api.add_resource(UserChannelResource, '/user_channels', '/user_channels/<int:user_channel_id>')
api.add_resource(AuthResource, '/login')



if __name__ == '__main__':
    app.run(port=5555, debug=True)

