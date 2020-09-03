import React from 'react';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

class DisclaimerPage extends React.Component {
    constructor(props) {
        super(props);


        this.state = {};

    }

    componentDidMount() {
        window.scrollTo(0, 0);        
    }
    
    render() {
        const {} = this.state;
        return (
            <Container className="docs">
                <Row>
                    <Col>
                    <div className="stackedit__html">
  <h2 id="parserx-disclaimer">ParseRx Disclaimer</h2>
  <p>
    This disclaimer applies to your use of the websites, mobile applications and
    other resources provided by ParseRx LLC and its affiliates (referred to
    collectively as “ParseRx”, “us,” “we” and “our”). By using the ParseRx
    service you agree to the terms of this disclaimer.
  </p>
  <p>
    ParseRx parses medication sigs from multiple sources, including healthcare
    organizations, third-party applications, and publicly available sources. The
    parsed sigs we offer are our best attempt at structuring free-text
    medication instructions; while we believe our data to be accurate,
    medication sigs are complex and vary widely, and we can’t guarantee the
    parsed sig we provide will exactly match your interpretation of the sig. It
    is your responsibility to use professional and clinical judgement before
    applying any of the sigs provided by ParseRx in clinical practice.
  </p>
  <h3 id="disclaimer">Disclaimer</h3>
  <p>
    All information provided by ParseRx is intended for U.S. healthcare
    professionals and students for educational purposes only and should only be
    used appropriately in the context of the provider’s legal role as a
    healthcare provider in their respective state and country. ParseRx LLC does
    not accept responsibility or liability for the application of this
    information in direct or indirect patient care, and such information should
    not be substituted for the advice, diagnosis, or treatment of a qualified
    health care professional. It is the responsibility of the healthcare
    provider to verify the accuracy of each parsed medication sig before using
    it in their clinical practice. The creators and reviewers have made every
    effort to provide accurate and complete information and shall not be held
    responsible for any damages or any losses from any error, possible omission,
    or inaccuracy. Therefore, ParseRx LLC shall not be held liable for any loss
    or injury caused by information obtained through this website, or API.
    ParseRx provides no warranty for any parsed sig data or other information.
    All trademarks, brands, logos and copyright images are property of their
    respective owners and rights holders. All data provided is for informational
    purposes only and is not meant to be a substitute for professional medical
    advice, diagnosis or treatment. Please seek medical advice before starting,
    changing or terminating any medical treatment.
  </p>
  <h3 id="liability">Liability</h3>
  <p>
    In no event will any of us or our respective directors, officers, employees,
    contractors, agents, sponsors, licensors or any other person or entity
    involved in creating, developing or delivering the ParseRx Services or
    Content be liable for any damages (including, without limitation, incidental
    and consequential damages, personal injury/wrongful death, lost profits, or
    damages resulting from lost data or business interruption) arising out of or
    in connection with these Terms or from the use of or inability to access or
    use ParseRx Content or Services, or from any communications or interactions
    with other persons with whom you communicate or interact as a result of your
    use of the Services, whether based on warranty, contract, tort, or any other
    legal theory, and whether or not we, our licensors, ours suppliers, or any
    third parties mentioned with the Services are advised of the possibility of
    such damages. We, our licensors, our suppliers, or any third parties
    mentioned within the Services are not liable for any personal injury,
    including death, caused by your use or misuse of the Services or any
    information provided through the Services. Any claims arising in connection
    with your use of the Services must be brought within one (1) year of the
    date of the event giving rise to such action occurred. Remedies under these
    Terms are exclusive and are limited to those expressly provided for in these
    Terms. The limitations of damages set forth above are fundamental elements
    of the basis of the bargain between us and you.
  </p>
  <h3 id="credits">Credits</h3>
  <p>Icons made by <a href="https://www.flaticon.com/authors/freepik">Freepik</a> from <a href="https://www.flaticon.com/">www.flaticon.com</a>.</p>
</div>


                    </Col>
                </Row>
            </Container>
        );
    }
}

export { DisclaimerPage }; 