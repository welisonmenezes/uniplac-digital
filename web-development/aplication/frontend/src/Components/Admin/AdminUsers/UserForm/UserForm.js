import React, { Component } from 'react';

class UserForm extends Component {

    constructor(props) {
        super(props);
        this.state = {};

        console.log(props);
    }

    render() {
        return (
            <div className="UserForm">
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h1>Admin user form</h1>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


export default UserForm;
