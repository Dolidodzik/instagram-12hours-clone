import React from 'react';
import Register from './components/register';
import Login from './components/login';

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

          <Route path="/register" component={Register}>
          </Route>

          <Route path="/login" component={Login}>
          </Route>

        </Switch>
      </Router>

    </div>
  );
}

export default App;
