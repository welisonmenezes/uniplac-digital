import React, { Component } from 'react';

import RichEditor from '../Shared/RichEditor/RichEditor';

class Dashboard extends Component {

  getEditorValue = (editorValue) => {
    //console.log('RichEditor Data: ', editorValue);
  };

  render() {
    return (
      <div className="Dashboard">
        <h1>Dashboard</h1>
        <hr />
        <RichEditor parentGettingTheEditorValue={this.getEditorValue} />
      </div>
    );
  }
}

export default Dashboard;
