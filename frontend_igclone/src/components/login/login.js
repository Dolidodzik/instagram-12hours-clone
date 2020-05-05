import React, {Component} from 'react';
import './login.css'

export default class Login extends Component {

    constructor(props){
      super(props);
      this.state = {
        username: '',
        password: '',
        areCredentialsIncorrect: false,
      };
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(e){

      const data = JSON.stringify({
        username: this.state.username,
        password: this.state.password,
      })

      console.log(data)

      fetch('http://localhost:8000/api/v0/token_auth/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: data,
			})
			.then((response) => response.json())
			.then((data) => {
         console.log(data)
				 if(data.token){
            localStorage.setItem('auth_token', data.token);
            this.props.history.push('/');
				 }else{
						this.setState({ areCredentialsIncorrect: true })
				 }
			})
			.catch((error) => {
				console.error('Error:', error);
			});

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
              <input type="password" className="form-control" placeholder="Password" name="password" required onChange={this.handleChange} />
          </div>

          <button type="submit" className="btn btn-primary">Submit</button>

          { this.state.areCredentialsIncorrect && <div> wrong password or login </div> }

        </form>
      )
    }
  }
