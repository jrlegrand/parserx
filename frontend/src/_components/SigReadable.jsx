import React from 'react';
import Card from 'react-bootstrap/Card'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPrescription } from '@fortawesome/free-solid-svg-icons'

const rxIcon = <FontAwesomeIcon icon={faPrescription} />

class SigReadable extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            sig_reviewed: this.props.sig_reviewed,
            sig_parsed: this.props.sig_parsed
        };
    }

    render() {
        const { sig_reviewed, sig_parsed } = this.state;
        console.log('sig_parsed', sig_parsed);
        return (
            <Card className="mb-3 rx-label">
                <Card.Body>
                    <span className="mr-3">{rxIcon}</span>
                    {sig_parsed.sig_readable && sig_parsed.sig_readable.toUpperCase()}
                </Card.Body>
            </Card>
        );
    }
}

export { SigReadable }