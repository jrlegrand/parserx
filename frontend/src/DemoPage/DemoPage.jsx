import React from 'react';
import { sigService } from '../_services';
import { SigParsed, SigHighlighted, SigReadable } from '../_components';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import InputGroup from 'react-bootstrap/InputGroup'
import FormControl from 'react-bootstrap/InputGroup'

class DemoPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
          user: {},
          value: '',
          sig: {}
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleReset = this.handleReset.bind(this);
    }

    componentDidMount() {
        window.scrollTo(0, 0);     
        this.setState({ 
          user: JSON.parse(localStorage.getItem('user')),
      });
 
    }

    handleChange(event) {
      this.setState({value: event.target.value});
    }
  
    handleSubmit(event) {
      this.setState({sig: {}});
      sigService.postSig(this.state.value)
      .then(
          sig => {
              this.setState({ sig })
              console.log(this.state.sig)
          },
          error => console.log(error)
      );

      event.preventDefault();
    }

    handleReset(event) {
      this.setState({sig: {}, value:''});

      event.preventDefault();
    }

      
    render() {
        const {user,value,sig} = this.state;
        return (
            <Container className="demo">
                <Row>
                    <Col>
                      <h1>Demo</h1>
                      <Form onSubmit={this.handleSubmit}>
                        <Form.Group>
                          <Form.Control type="text" placeholder="Enter sig text here" value={value} onChange={this.handleChange} />
                          <div className="mt-3">
                            <Button variant="primary" type="submit">
                              Submit
                            </Button>
                            {sig.sig_parsed &&
                            <Button variant="secondary" type="button" className="ml-2" onClick={this.handleReset}>
                              Reset
                            </Button>
                            }
                          </div>
                        </Form.Group>
                      </Form>
                      {sig.sig_parsed && <SigHighlighted sig_parsed={sig.sig_parsed[0]} user={user} />}
                      {sig.sig_parsed && <SigReadable sig_parsed={sig.sig_parsed[0]} user={user} />}
                      {sig.sig_parsed && <SigParsed sig_parsed={sig.sig_parsed[0]} user={user} />}
                      {sig.sig_parsed && <pre><code>{JSON.stringify(sig.sig_parsed,null,2)}</code></pre>}
                    </Col>
                </Row>
            </Container>
        );
    }
}

export { DemoPage }; 