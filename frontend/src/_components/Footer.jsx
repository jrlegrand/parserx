import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import { userService } from '../_services';

class Footer extends React.Component {
    constructor(props) {
        super(props);
    }
    
    render() {
        const { isLoggedIn } = this.props;
        return (
            <div className="footer">
                <Container>
                    <Row>
                    <Col>
                        <p>&copy; 2022 ParseRx</p>
                        <Link to="/disclaimer">Disclaimer</Link><br/>
                        <Link to="/terms-of-service">Terms Of Service</Link><br/>
                        <Link to="/privacy-policy">Privacy Policy</Link>
                    </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

export { Footer }