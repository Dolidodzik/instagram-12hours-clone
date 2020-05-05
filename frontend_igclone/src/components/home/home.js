import React, {Component} from 'react';
import './home.css'

export default class Home extends Component {

    constructor(props){
      super(props);
      this.state = {
        posts: null
      }
      this.requestFeed = this.requestFeed.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount(){
      this.requestFeed();
    }

    requestFeed(e){
      fetch("http://localhost:8000/api/v0/posts/", {
        headers: {
           'Authorization': 'Token ' + localStorage.getItem('auth_token'),
           'Content-Type': 'application/json',
        }
      })
      .then(res => res.json())
      .then((result) => {
        this.setState({
          posts: result
        })
      })
    }

    handleSubmit(e, post_id, i){

      const data = JSON.stringify({
        text: this.state.comment_text,
        post: post_id
      })

      fetch('http://localhost:8000/api/v0/comments/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token ' + localStorage.getItem('auth_token'),
        },
        body: data,
      })
      .then((response) => response.json())
      .then((data) => {
        console.log(this.state.posts[i].comments)
        console.log(data)
        console.log()
        if(data[0].id){
          let posts = this.state.posts;
          let comments = data.concat(this.state.posts[i].comments)
          posts[i].comments = comments
          this.setState({
            posts: posts
          })
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
      e.preventDefault();
    }

    handleChange(event){
      console.log(event)
      this.setState({ comment_text: event.target.value, comment_post: 1 });
      return true;
    }

    renderComments(post){
      if(post.comments){
        return(
          <div>
            {post.comments.map((comment, j) =>
              <div obj={post} key={j} style={{padding: 10, margin: 5, backgroundColor: "#aed"}}>
                Posted by: <img src={"http://localhost:8000"+comment.owner_profile_photo} width="50px" /> {comment.owner_username}
                <br/>
                text: {comment.text}

              </div>
            )}
          </div>
        )
      }
    }

    render() {
      if(this.state.posts){
        return (
          <div>
            {this.state.posts.map((post, i) =>
              <div obj={post} key={i} style={{padding: 50, margin: 10, backgroundColor: "#876"}}>
                Posted by: <img src={"http://localhost:8000"+post.owner_profile_photo} width="100px" /> {post.owner_username}
                <br/>
                Title: {post.title}
                description: {post.description}
                hearts: {post.likesCount}
                <br/>

                <form onSubmit={(e) => this.handleSubmit(e, post.id, i)}>

                  <div className="form-group">
                      <label> Your comment: </label>
                      <input type="text" className="form-control" placeholder="your comment" name="comment_content" required onChange={this.handleChange} />
                  </div>


                  <button type="submit" className="btn btn-primary">Submit</button>

                  { this.state.areCredentialsIncorrect && <div> wrong password or login </div> }

                </form>

                Comments:
                {this.renderComments(post)}

              </div>
            )}
          </div>
        );
      }else{
        return (
          <div> loading </div>
        );
      }
    }
  }
