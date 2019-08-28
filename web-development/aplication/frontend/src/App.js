import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';

// public components
import Home from './Components/Public/Home/Home';
import NotFound from './Components/Public/NotFound/NotFound';
import Login from './Components/Public/Login/Login';

// admin components
import Dashboard from './Components/Admin/Dashboard/Dashboard';

// utils/extras
import PrivateRouter from './Utils/PrivateRouter';

class App extends Component {
  render() {
    return (
      <div className="App">
          <Switch>
            <Route path="/" exact={true} component={Home} />
            <Route path='/login' exact={true} component={Login} />
            <PrivateRouter path='/admin' component={Dashboard} />
            <Route path='*' component={NotFound} />
          </Switch>
      </div>
    );
  }
}

export default App;
