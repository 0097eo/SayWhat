import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const AllPosts = () => {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/posts')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setPosts(data);
        setIsLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setIsLoading(false);
      });
  }, []);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="all-posts">
      <h2>Explore</h2>
      {posts.map(post => (
        <div key={post.id} className="post-preview">
          <h3><Link to={`/posts/${post.id}`}>{post.title}</Link></h3>
          <p>By: {post.author.username}</p>
          <p>{post.content.substring(0, 100)}...</p>
          <p>Created: {new Date(post.created_at).toLocaleDateString()}</p>
        </div>
      ))}
    </div>
  );
}

export default AllPosts;