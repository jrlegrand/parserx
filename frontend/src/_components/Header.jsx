import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import { userService } from '../_services';

class Header extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            isLoggedIn: this.props.isLoggedIn
        };
    }

    render() {
        const { isLoggedIn } = this.state;
        return (
            <Navbar collapseOnSelect expand="md" fixed="top" bg="light" variant="light">
                <Container>
                <Navbar.Brand as={Link} to="/" id="logo">ParseRx</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                    <Navbar.Collapse id="responsive-navbar-nav">
                        <Nav className="mr-auto">
                            { 1 == 0 && <Nav.Link as={Link} to="/sig">Sig</Nav.Link> }
                        </Nav>
                        <Nav>
                            { !isLoggedIn && <Nav.Link href="#contact">Contact</Nav.Link>}
                            { isLoggedIn && <Nav.Link as={Link} to="logout">Logout</Nav.Link>}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        );
    }
}

export { Header }