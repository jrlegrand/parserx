import React from 'react';

import { sigService } from '../_services';
import { SigParsed, SigHighlighted, SigReadable } from '../_components';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import Pagination from 'react-bootstrap/Pagination';

class SigPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: {},
            sigs: [],
            page: 1,
            perPage: 10,
            siblingCount: 2,
        };

        this.handleGetSigs = this.handleGetSigs.bind(this)
        this.pagination = this.pagination.bind(this)
    }

    componentDidMount() {
        this.setState({ 
            user: JSON.parse(localStorage.getItem('user')),
        });
        this.handleGetSigs(this.state.page);
    }

    handleGetSigs(page) {
        const { perPage } = this.state;
        this.setState({ 
            sigs: { loading: true }
        });
        sigService.getSigs(page).then(sigs => {
            const count = sigs.count;
            const totPages = Math.ceil(count/perPage);
            this.setState({ sigs, page, count, totPages });
        });
    }

    pagination() {
        const { page, totPages, loading,siblingCount, perPage } = this.state;
        const range = (start, stop, step) => Array.from({ length: (stop - start) / step + 1}, (_, i) => start + (i * step));
        const earlyRange = range(1,Math.min(10, totPages),1);
        const middleRange = range(page-siblingCount,Math.min(page+siblingCount,totPages),1);
        const endRange = range(totPages-9,totPages,1);

        return (
            <>
            { !loading && (

            <Pagination>
                { page > 1 && <>
                <Pagination.Prev onClick={() => this.handleGetSigs(page-1)} /></> }

                { page <= 10 && earlyRange.map((p) => (
                    <Pagination.Item active={p == page} onClick={() => this.handleGetSigs(p)}>{p}</Pagination.Item>    
                ))}

                { page > 10 && <>
                <Pagination.Item onClick={() => this.handleGetSigs(1)}>{1}</Pagination.Item>
                <Pagination.Ellipsis />
                </>
                }

                { page > 10 && (page <= (totPages - 10) || (page <= totPages && totPages < 2*perPage)) && middleRange.map((p) => (
                    <Pagination.Item active={p == page} onClick={() => this.handleGetSigs(p)}>{p}</Pagination.Item>    
                ))}

                { (page <= (totPages - 10) || (page < totPages && totPages < 2*perPage && page < (totPages - siblingCount))) && <>
                {page != (totPages - siblingCount - 1) && (<Pagination.Ellipsis />)}
                <Pagination.Item onClick={() => this.handleGetSigs(totPages)}>{totPages}</Pagination.Item>
                <Pagination.Next onClick={() => this.handleGetSigs(page+1)} />
                </> }

                { page > (totPages - 10) && totPages > 2*perPage && endRange.map((p) => (
                    <Pagination.Item active={p == page} onClick={() => this.handleGetSigs(p)}>{p}</Pagination.Item>    
                ))}

           

            </Pagination>
        )}
        </>
        )
    }

    render() {
        const { user, sigs, page } = this.state;
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
                        <p>Page {page} · {sigs.count} sigs to review.</p>
                        {sigs.results.map((sig, index) =>
                            <div key={"sig_" + sig.id} className="sig-parsed-review">
                                <Row>
                                    <Col xs={12}>
                                        {sig.sig_parsed && <SigHighlighted sig_parsed={sig.sig_parsed[0]} user={user} />}
                                    </Col>
                                </Row>
                                {sig.sig_parsed.length > 0 &&
                                    <>
                                        <SigReadable sig_parsed={sig.sig_parsed[0]} user={user} />
                                        <SigParsed sig_parsed={sig.sig_parsed[0]} user={user} />
                                    </>
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
                        { this.pagination() }
                    </Col>
                </Row>
                </Container>
            </div>
        );
    }
}

export { SigPage };