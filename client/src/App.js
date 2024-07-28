import NotFound from './Components/NotFound';
import NavBar from './Components/NavBar';
import { Routes, Route } from 'react-router-dom';
import AllPosts from './Components/AllPosts';
import PostDetails from './Components/PostDetails';

function App() {
  return (
    <div className="App">
        <NavBar />
        <p>SayWhat Now</p>
        <Routes>
          <Route exact path="/" element={<AllPosts/>} />
          <Route exact path="/about" element={<h1>About</h1>} />
          <Route exact path="/posts/:id" element={<PostDetails/>} />
          <Route path="*" element={<NotFound />} />
        </Routes>
    </div>
  );
}

export default App;
