import React, { Component } from 'react';

import Navigation from '../Shared/Navigation/Navigation';

class NotFound extends Component {

  render() {
    return (
      <div className="NotFound">
        <Navigation></Navigation>
        <h1>NotFound</h1>
      </div>
    );
  }
}

export default NotFound;
