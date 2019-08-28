import React, { Component } from 'react';

import Navigation from '../../Public/Shared/Navigation/Navigation';
import RichEditor from '../Shared/RichEditor/RichEditor';

class Dashboard extends Component {

  render() {
    return (
      <div className="Dashboard">
        <Navigation></Navigation>
        <h1>Dashboard</h1>
        <hr />
        <RichEditor />
      </div>
    );
  }
}

export default Dashboard;
