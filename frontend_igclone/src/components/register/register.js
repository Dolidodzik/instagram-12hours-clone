import React, {Component} from 'react';
import './register.css'

export default class Register extends Component {

    constructor(props){
      super(props);
      this.state = {
          username: '',
          email: '',
          newPassword: '',
          newPasswordRepeat: '',

          emailTaken: false,
          usernameTaken: false,
          passwordsNotTheSame: false,
          success: false,
      };
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(e){
      if(this.newPassword != this.newPasswordRepeat){
        this.setState({
          passwordsNotTheSame: true
        })
      }

      const data = JSON.stringify({
        username: this.state.username,
        first_name: "",
        last_name: "",
        email: this.state.email,
        followersCount: null,
        followedCount: null,
        description: "",
        profile_image: null,
        chatted_with: "",
        password: this.state.newPassword,
        password_confirm: this.state.newPasswordRepeat
      })

      console.log(data)

      fetch("http://localhost:8000/api/v0/accounts/register/", {
        method: 'POST',
        body: data,
        headers: {
          'Content-Type': 'application/json',
        }
      })
      .then(res => res.json())
      .then((result) => {
        console.log(result)
        if(result.id){
          this.setState({
            success: true
          });
        }
      })

      e.preventDefault();
    }
    handleChange(event){
      const target = event.target;
      const value = target.type === 'checkbox' ? target.checked : target.value;
      const name = target.name;
      this.setState({ [name]: value });
      return true;
    }

    render() {
      return (
        <form onSubmit={this.handleSubmit}>
          <div className="form-group">
              <label>Username</label>
              { this.state.usernameTaken && <div> this username is already taken </div> }
              <input type="text" className="form-control" placeholder="Username" name="username" required onChange={this.handleChange} />
          </div>
          <div className="form-group">
              <label>Password</label>
              <input type="password" className="form-control" placeholder="Password" name="newPassword" required onChange={this.handleChange} />
          </div>
          <div className="form-group">
              <label>Password repeat { this.state.passwordsNotTheSame && <div> passwords are not the same </div> } </label>
              <input type="password" className="form-control" placeholder="Password repeat" name="newPasswordRepeat" required onChange={this.handleChange} />
          </div>
          <div className="form-group">
              <label>Email</label>
              { this.state.emailTaken && <div> this email is already taken </div> }
              <input type="email" className="form-control" placeholder="email" name="email" required onChange={this.handleChange} />
          </div>


          <button type="submit" className="btn btn-primary">Submit</button>

          { this.state.success && <div> created account succesfully, here you can <a href="/login">login</a> </div> }

        </form>
      )
    }
  }
