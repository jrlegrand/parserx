import React from 'react';

import { sigService } from '../_services';
import { SigParsed, SigHighlighted } from '../_components';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';

class SigPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: {},
            sigs: [],
            page: 1
        };

        this.handleGetSigs = this.handleGetSigs.bind(this)
    }

    componentDidMount() {
        this.setState({ 
            user: JSON.parse(localStorage.getItem('user')),
        });
        this.handleGetSigs(this.state.page);
    }

    handleGetSigs(page) {
        this.setState({ 
            sigs: { loading: true }
        });
        sigService.getSigs(page).then(sigs => this.setState({ sigs, page }));       
    }

    render() {
        const { user, sigs, page } = this.state;
        console.log(sigs);
        console.log(user);
        return (
            <div>
                <Container>
                <Row>
                    <Col>
                        <h1>Sig Review</h1>
                        {sigs.loading && 
                            <Spinner animation="border" role="status">
                                <span className="sr-only">Loading...</span>
                            </Spinner>
                        }
                    </Col>
                </Row>
                {sigs.results &&
                    <div>
                        <p>{sigs.count} sigs to review.</p>
                        {sigs.results.map((sig, index) =>
                            <div key={"sig_" + sig.id} className="sig-parsed-review">
                                <Row>
                                    <Col xs={12}>
                                        {sig.sig_parsed && <SigHighlighted sig_parsed={sig.sig_parsed[0]} user={user} />}
                                    </Col>
                                </Row>
                                {sig.sig_parsed.length > 0 &&
                                    <SigParsed sig_parsed={sig.sig_parsed[0]} user={user} />
                                }
                                {sig.sig_parsed.length > 1 && 
                                    <Accordion>
                                            <Accordion.Toggle as={Button} variant="link" eventKey={"history_" + sig.id}>
                                                <span className="material-icons">history</span> {sig.sig_parsed.length - 1}
                                            </Accordion.Toggle>
                                            <Accordion.Collapse eventKey={"history_" + sig.id}>
                                                <div>
                                                    {sig.sig_parsed.map((sig_parsed, index) =>
                                                        <div key={"historical_" + sig_parsed.id}>
                                                            {index > 0 &&
                                                                <div>
                                                                    <small><strong>Created:</strong> {sig_parsed.created}</small>
                                                                    <SigParsed sig_parsed={sig_parsed} user={user} />
                                                                </div>
                                                            }
                                                        </div>
                                                    )}
                                                </div>
                                            </Accordion.Collapse>
                                    </Accordion>
                                }
                            </div>
                        )}
                    </div>
                }
                <Row>
                    <Col>
                        {sigs.previous && 
                            <span>
                                <button onClick={() => this.handleGetSigs(page - 1)}>Get previous page of sigs</button>
                            </span>
                        }
                        {sigs.next && 
                            <span>
                                <button onClick={() => this.handleGetSigs(page + 1)}>Get next page of sigs</button>
                            </span>
                        }
                    </Col>
                </Row>
                </Container>
            </div>
        );
    }
}

export { SigPage };