import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import { userService } from '../_services';

class Header extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const { isLoggedIn } = this.props;
        return (
            <Navbar collapseOnSelect expand="md" fixed="top" bg="light" variant="light">
                <Container>
                <Navbar.Brand as={Link} to="/" id="logo">ParseRx</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                    <Navbar.Collapse id="responsive-navbar-nav">
                        <Nav className="mr-auto">
                            { 1 == 0 && <></> }
                        </Nav>
                        <Nav>
                            <Nav.Link as={Link} to="docs" className="mr-2">Documentation</Nav.Link>
                            { !isLoggedIn && ( 
                                <Link to="/login">
                                    <Button size="md" variant="outline-dark">Login</Button>{' '}
                                </Link>
                            )}
                            { isLoggedIn && (
                                <>
                                <Nav.Link as={Link} to="sig" className="mr-2">Review</Nav.Link>
                                <Nav.Link as={Link} to="demo" className="mr-2">Demo</Nav.Link>
                                <Link to="/logout">
                                    <Button size="md" variant="outline-dark">Logout</Button>{' '}
                                </Link>
                                </>
                            )}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        );
    }
}

export { Header }