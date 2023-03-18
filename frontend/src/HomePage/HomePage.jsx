import React from 'react';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Carousel from 'react-bootstrap/Carousel';

import rxPad from '../assets/images/pharmacy-icons/svg/044-rx.svg';
import pillBottle from '../assets/images/pharmacy-icons/svg/028-container.svg';
import medicalFolder from '../assets/images/pharmacy-icons/svg/006-medical folder.svg';
import phoneConsultation from '../assets/images/pharmacy-icons/svg/050-consultation.svg';

import '../assets/css/parserx.css'

import { userService } from '../_services';

class HomePage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <div>
            <Container className="hero d-flex align-items-center">
            <Row>
                <Col md={6}>
                    <div>
                        <h1>Medication sig parser</h1>
                        <p>Designed, built, and tested by a pharmacist to structure free-text medication sigs.</p>
                        <ul className="fa-ul">
                            <li><span className="fa-li"><span className="material-icons green">done</span></span> Parse dose, frequency, duration, and more from medication sigs</li>
                            <li><span className="fa-li"><span className="material-icons green">done</span></span> Calculate total dose to power clinical decision support</li>
                            <li><span className="fa-li"><span className="material-icons green">done</span></span> Save valuable clinician time by automating medication sig entry</li>
                        </ul>
                    </div>
                </Col>
                <Col md={6} className="text-center">
                    <img width="75%" src={rxPad} />
                </Col>
            </Row>
            </Container>

            <div class="text-center carousel-header">
                <h1>Make sense of your sigs</h1>
            </div>
            <Carousel>
                <Carousel.Item>
                    <Container>
                    <Row className="carousel-sig d-flex align-items-center">
                        <Col md={6} className="sig">
                            <span className="highlight-red">take</span> <span className="highlight-orange">1-2 tablets</span> <span className="highlight-yellow">po</span> <span className="highlight-green">qid</span> <span className="highlight-blue">x6d</span> <span className="highlight-purple">prn nausea</span>
                        </Col>
                        <Col md={6} className="sig-parsed">
                            <ul className="fa-ul">
                                <li><span className="material-icons red">arrow_forward</span> <strong>method:</strong> take</li>
                                <li><span className="material-icons orange">arrow_forward</span> <strong>dose_min:</strong> 1, <strong>dose_max:</strong> 2, <strong>dose_unit:</strong> tablet</li>
                                <li><span className="material-icons yellow">arrow_forward</span> <strong>route:</strong> oral</li>
                                <li><span className="material-icons green">arrow_forward</span> <strong>frequency:</strong> 4, <strong>period:</strong> 1, <strong>period_unit:</strong> d</li>
                                <li><span className="material-icons blue">arrow_forward</span> <strong>duration:</strong> 6, <strong>duration_unit:</strong> d</li>
                                <li><span className="material-icons purple">arrow_forward</span> <strong>as_needed:</strong> true, <strong>as_needed_indication:</strong> nausea</li>
                            </ul>                            
                        </Col>
                    </Row>
                    </Container>
                </Carousel.Item>
                <Carousel.Item>
                    <Container>
                    <Row className="carousel-sig d-flex align-items-center">
                        <Col md={6} className="sig">
                            <span className="highlight-red">inhale</span> <span className="highlight-orange">two or four puffs</span> <span className="highlight-yellow"></span> <span className="highlight-green">every 4-6 hours</span> <span className="highlight-purple">as needed for wheezing</span>                        </Col>
                        <Col md={6} className="sig-parsed">
                            <ul className="fa-ul">
                                <li><span className="material-icons red">arrow_forward</span> <strong>method:</strong> inhale</li>
                                <li><span className="material-icons orange">arrow_forward</span> <strong>dose_min:</strong> 2, <strong>dose_max:</strong> 4, <strong>dose_unit:</strong> pressurized inhalation</li>
                                <li><span className="material-icons green">arrow_forward</span> <strong>frequency:</strong> 1, <strong>period:</strong> 4, <strong>period_max:</strong> 6, <strong>period_unit:</strong> h</li>
                                <li><span className="material-icons purple">arrow_forward</span> <strong>as_needed:</strong> true, <strong>as_needed_indication:</strong> wheezing</li>
                            </ul>                            
                        </Col>
                    </Row>
                    </Container>
                </Carousel.Item>
                <Carousel.Item>
                    <Container>
                    <Row className="carousel-sig d-flex align-items-center">
                        <Col md={6} className="sig">
                        <span className="highlight-red">inject</span> <span className="highlight-orange">1 pen (40mg)</span> <span className="highlight-yellow">under the skin</span> <span className="highlight-green">every other week</span>
                        </Col>
                        <Col md={6} className="sig-parsed">
                            <ul className="fa-ul">
                                <li><span className="material-icons red">arrow_forward</span> <strong>method:</strong> inject</li>
                                <li><span className="material-icons orange">arrow_forward</span> <strong>dose:</strong> 1, <strong>dose_unit:</strong> pen, <strong>dose_strength:</strong> 40, <strong>dose_strength_unit:</strong> mg</li>
                                <li><span className="material-icons yellow">arrow_forward</span> <strong>route:</strong> subcutaneous</li>
                                <li><span className="material-icons green">arrow_forward</span> <strong>frequency:</strong> 1, <strong>period:</strong> 2, <strong>period_unit:</strong> wk</li>
                            </ul>                            
                        </Col>
                    </Row>
                    </Container>
                </Carousel.Item>
            </Carousel>
            <Container>
            <Row className="featurette">
                <Col md={{ span: 6, order: 2 }} className="text-center">
                    <img width="50%" src={pillBottle} />
                </Col>
                <Col md={{ span: 6, order: 1 }}>
                    <h1>Built to support a variety of uses</h1>
                    <h3><span className="material-icons orange">emoji_objects</span> Decision support</h3>
                    <p>Unlock valuable clinical information to provide medication dosing support.</p>
                    <h3><span className="material-icons green">insert_chart</span> Data analysis</h3>
                    <p>Inform important decisions with clean, structured medication sig data.</p>
                    <h3><span className="material-icons purple">local_pharmacy</span> Clinical workflows</h3>
                    <p>Reduce unnecessary clicks and keystrokes by automating medication reconciliation processes.</p>
                </Col>
            </Row>

            <Row className="featurette">
                <Col md={6} className="text-center">
                    <img width="50%" src={medicalFolder} />
                </Col>
                <Col md={6}>
                    <h1>Choose a service to fit your needs</h1>
                    <h3><span className="material-icons blue">api</span> REST API</h3>
                    <p>Use our API for your custom application to dynamically parse medication sigs.</p>
                    <h3><span className="material-icons red">table_chart</span> Batch parsing</h3>
                    <p>Convert a spreadsheet of medication sigs to their structured equivalents.</p>
                    <h3><span className="material-icons green">storage</span> Database licensing</h3>
                    <p>Utilize our full database of parsed and validated sigs to drive translation tables in your EHR.</p>
                </Col>
            </Row>

            </Container>
            </div>
        );
    }
}

export { HomePage }; 