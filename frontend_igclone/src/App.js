import React from 'react';
import Register from './components/register';


import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";


function App() {
  return (
    <div className="App">

      <Router>
        <Switch>

          <Route path="/register">
            <Register />
          </Route>

        </Switch>
      </Router>

    </div>
  );
}

export default App;
