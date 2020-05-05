import React, {Component} from 'react';
import './home.css'

export default class Home extends Component {

    constructor(props){
      super(props);
      this.state = {
        posts: null
      }
      this.requestFeed = this.requestFeed.bind(this);
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

    render() {
      if(this.state.posts){
        return (
          <div>
            {this.state.posts.map((object, i) =>
              <div obj={object} key={i}>
                Title: {object.title}
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
