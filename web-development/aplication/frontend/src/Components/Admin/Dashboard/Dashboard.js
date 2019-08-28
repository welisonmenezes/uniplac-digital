import React, { Component } from 'react';

import Navigation from '../../Public/Shared/Navigation/Navigation';

class Dashboard extends Component {

  render() {
    return (
      <div className="Dashboard">
        <Navigation></Navigation>
        <h1>Dashboard</h1>
      </div>
    );
  }
}

export default Dashboard;
