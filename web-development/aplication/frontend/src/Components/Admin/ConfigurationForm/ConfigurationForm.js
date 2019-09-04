import React, { Component } from 'react';

import Navigation from '../Shared/Navigation/Navigation';

class ConfigurationForm extends Component {

    constructor(props) {
        super(props);
        this.state = {};

        console.log(props);
    }

    render() {
        return (
            <div className="ConfigurationForm">
                <Navigation></Navigation>
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h1>Admin config form</h1>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


export default ConfigurationForm;
