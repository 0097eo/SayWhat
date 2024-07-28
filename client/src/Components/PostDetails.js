import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import './PostDetails.css';

const PostDetails = () => {
  const [post, setPost] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    fetch(`/posts/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setPost(data);
        setIsLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setIsLoading(false);
      });
  }, [id]);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!post) return <div>No post found</div>;

  return (
    <div className="post-details">
      <h2>{post.title}</h2>
      <p className="author">By: {post.author.username}</p>
      <p className="date">Created: {new Date(post.created_at).toLocaleString()}</p>
      <div className="content">{post.content}</div>
      <h3>Comments</h3>
      {post.comments && post.comments.length > 0 ? (
        <ul className="comments">
          {post.comments.map(comment => (
            <li key={comment.id} className="comment">
              <p>{comment.content}</p>
              <p className="comment-author">- {comment.author.username}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No comments yet.</p>
      )}
      <Link to="/" className="back-link">Back to All Posts</Link>
    </div>
  );
}

export default PostDetails;