import React from 'react';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { userService } from '../_services';

class LogoutPage extends React.Component {
    constructor(props) {
        super(props);

        userService.logout();

        this.state = {
            loading: true,
        };

    }
    
    componentDidMount() {
        window.scrollTo(0, 0);        
        userService.logout();
        this.props.history.push("/");
    }

    render() {
        const { loading, error } = this.state;
        return (
          <p>You are being logged out...</p>
        );
    }
}

export { LogoutPage }; 