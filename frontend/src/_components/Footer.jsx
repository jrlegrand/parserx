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
                        <p>&copy; ParseRx</p>
                    </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

export { Footer }