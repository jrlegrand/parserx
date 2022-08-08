import React from 'react';
import { SigReviewedOverall, SigReviewedPart } from '../_components';
import { sigService } from '../_services';
import Table from 'react-bootstrap/Table';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class SigParsed extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            sig_parsed: this.props.sig_parsed,
            sig_reviewed: this.props.sig_parsed.sig_reviewed.filter(sig_reviewed => sig_reviewed.owner == this.props.user.id )[0],
            sig_parsed_components: {},
            user: this.props.user
        };
        
        this.handleReview = this.handleReview.bind(this);
        this.setSigComponents = this.setSigComponents.bind(this);
    }

    componentDidMount() {
        this.setSigComponents();
    }
    
    setSigComponents() {
        // TODO: move this to a separate componennt called SigHighlighted
        // TODO: make this work - right now it just returns the sig_text with no highlighting
        // keep in mind that these components could overlap...
        const sig_parsed = this.state.sig_parsed;
        const sig_parsed_components = {
            method: {
                method: sig_parsed.method,
                method_text: sig_parsed.method_text,
                method_text_start: sig_parsed.method_text_start,
                method_text_end: sig_parsed.method_text_end ,
                method_readable: sig_parsed.method_readable               
            },
            dose: {
                dose: sig_parsed.dose,
                dose_max: sig_parsed.dose_max,
                dose_unit: sig_parsed.dose_unit,
                dose_text: sig_parsed.dose_text,
                dose_text_start: sig_parsed.dose_text_start,
                dose_text_end: sig_parsed.dose_text_end,
                dose_readable: sig_parsed.dose_readable               
            },
            strength: {
                strength: sig_parsed.strength,
                strength_max: sig_parsed.strength_max,
                strength_unit: sig_parsed.strength_unit,
                strength_text: sig_parsed.strength_text,
                strength_text_start: sig_parsed.strength_text_start,
                strength_text_end: sig_parsed.strength_text_end,
                strength_readable: sig_parsed.strength_readable               
            },
            route: {
                route: sig_parsed.route,
                route_text: sig_parsed.route_text,
                route_text_start: sig_parsed.route_text_start,
                route_text_end: sig_parsed.route_text_end,             
                route_readable: sig_parsed.route_readable               
            },
            frequency: {
                frequency: sig_parsed.frequency,
                frequency_max: sig_parsed.frequency_max,
                period: sig_parsed.period,
                period_max: sig_parsed.period_max,
                period_unit: sig_parsed.period_unit,
                time_duration: sig_parsed.time_duration,
                time_duration_unit: sig_parsed.time_duration_unit,
                day_of_week: sig_parsed.day_of_week,
                time_of_day: sig_parsed.time_of_day,
                offset: sig_parsed.offset,
                bounds: sig_parsed.bounds,
                count: sig_parsed.count,
                frequency_text: sig_parsed.frequency_text,
                frequency_text_start: sig_parsed.frequency_text_start,
                frequency_text_end: sig_parsed.frequency_text_end,
                frequency_readable: sig_parsed.frequency_readable
            },
            when: {
                when: sig_parsed.when,
                when_text: sig_parsed.when_text,
                when_text_start: sig_parsed.when_text_start,
                when_text_end: sig_parsed.when_text_end,
                when_readable: sig_parsed.when_readable               
            },
            duration: {
                duration: sig_parsed.duration,
                duration_max: sig_parsed.duration_max,
                duration_unit: sig_parsed.duration_unit,
                duration_text: sig_parsed.duration_text,
                duration_text_start: sig_parsed.duration_text_start,
                duration_text_end: sig_parsed.duration_text_end,
                duration_readable: sig_parsed.duration_readable               
            },
            indication: {
                as_needed: sig_parsed.as_needed,
                indication: sig_parsed.indication,
                indication_text: sig_parsed.indication_text,
                indication_text_start: sig_parsed.indication_text_start,
                indication_text_end: sig_parsed.indication_text_end,
                indication_readable: sig_parsed.indication_readable               
            },
            max: {
                max_numerator_value: sig_parsed.max_numerator_value,
                max_numerator_unit: sig_parsed.max_numerator_unit,
                max_denominator_value: sig_parsed.max_denominator_value,
                max_denominator_unit: sig_parsed.max_denominator_unit,
                max_text_start: sig_parsed.max_text_start,
                max_text_end: sig_parsed.max_text_end,
                max_text: sig_parsed.max_text,
                max_readable: sig_parsed.max_readable
            },
            additional_info: {
                additional_info: sig_parsed.additional_info,
                additional_info_text_start: sig_parsed.additional_info_text_start,
                additional_info_text_end: sig_parsed.additional_info_text_end,
                additional_info_text: sig_parsed.additional_info_text,
                additional_info_readable: sig_parsed.additional_info_readable
            }
        };

        this.setState({ sig_parsed_components });
    }

    handleReview(val, e) {
        const user = this.state.user;
        const sig_reviewed = this.state.sig_reviewed;
        const { name, value } = e.target;
        if (name == 'sig_correct' && value == true) {
            
        }
        if (sig_reviewed) {
            sig_reviewed[name] = value;
            
            sigService.updateSigReviewed(sig_reviewed, user)
                .then(
                    sig_reviewed => {
                        this.setState({ sig_reviewed })
                    },
                    error => console.log(error)
                );
        } else {
            const sig_parsed = this.state.sig_parsed
            const sig_reviewed = { sig_parsed: sig_parsed.id }
            sig_reviewed[name] = value;

            sigService.createSigReviewed(sig_reviewed, user)
                .then(
                    sig_reviewed => {
                        this.setState({ sig_reviewed })
                    },
                    error => console.log(error) 
                );
        }        
    }

    render() {
        const { sig_parsed, sig_reviewed, sig_parsed_components } = this.state;
        return (
            <Row>
                <Col sm={12} md={10}>
                    <Table responsive borderless size="sm">
                        <thead> 
                            <tr>
                                <th>
                                    method
                                </th>
                                <th>
                                    dose
                                </th>
                                <th>
                                    strength
                                </th>
                                <th>
                                    route
                                </th>
                                <th>
                                    frequency
                                </th>
                                <th>
                                    duration
                                </th>
                                <th>
                                    indication
                                </th>
                                <th>
                                    max
                                </th>
                                <th>
                                    additional info
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td title={JSON.stringify(sig_parsed_components.method, null, 2)}>
                                    {sig_parsed.method_readable}
                                </td>
                                <td title={JSON.stringify(sig_parsed_components.dose, null, 2)}>
                                    {sig_parsed.dose_readable}
                                </td>
                                <td title={JSON.stringify(sig_parsed_components.strength, null, 2)}>
                                    {sig_parsed.strength_readable}
                                </td>
                                <td title={JSON.stringify(sig_parsed_components.route, null, 2)}>{sig_parsed.route}</td>
                                <td><span title={JSON.stringify(sig_parsed_components.frequency, null, 2)}>{sig_parsed.frequency_readable}</span>{sig_parsed.when && <span title={JSON.stringify(sig_parsed_components.when, null, 2)}>{" " + sig_parsed.when}</span>}</td>
                                <td title={JSON.stringify(sig_parsed_components.duration, null, 2)}>
                                    {sig_parsed.duration_readable}
                                </td>
                                <td title={JSON.stringify(sig_parsed_components.indication, null, 2)}>
                                    {sig_parsed.indication_readable}
                                </td>
                                <td title={JSON.stringify(sig_parsed_components.max, null, 2)}>
                                    {sig_parsed.max_readable}
                                </td>
                                <td title={JSON.stringify(sig_parsed_components.additional_info, null, 2)}>
                                    {sig_parsed.additional_info_readable}
                                </td>
                            </tr>
                            {sig_reviewed && !sig_reviewed.sig_correct &&
                            <tr>
                            {["method","dose","strength","route","frequency","duration","indication"].map(sig_part =>
                                    <td key={sig_part + "_" + sig_parsed.id}>
                                        <SigReviewedPart sig_part={sig_part} sig_reviewed={sig_reviewed} sig_parsed={sig_parsed} handleChange={this.handleReview} />
                                    </td>
                                )}
                            </tr>
                            } 
                        </tbody>
                    </Table>   
                </Col>
                <Col sm={12} md={2}>
                    <SigReviewedOverall sig_reviewed={sig_reviewed} sig_parsed={sig_parsed} handleChange={this.handleReview} />
                </Col>             
            </Row>
        );
    }
}

export { SigParsed }