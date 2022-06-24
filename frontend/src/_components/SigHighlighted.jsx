import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class SigHighlighted extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            sig_parsed: this.props.sig_parsed,
            sig_reviewed: this.props.sig_parsed.sig_reviewed.filter(sig_reviewed => sig_reviewed.owner == this.props.user.id )[0],
            user: this.props.user
        };
        
        this.setSigComponents = this.setSigComponents.bind(this);
    }

    componentDidMount() {
        this.setSigComponents();
    }

    getClassName(pos) {
        let className = [];
        const sig_parsed_components = this.state.sig_parsed_components;
        const method = sig_parsed_components.method;
        const dose = sig_parsed_components.dose;
        const strength = sig_parsed_components.strength;
        const route = sig_parsed_components.route;
        const frequency = sig_parsed_components.frequency;
        const when = sig_parsed_components.when;
        const duration = sig_parsed_components.duration;
        const indication = sig_parsed_components.indication;

        if (method.method_text_start != null && pos >= method.method_text_start && pos <= method.method_text_end) {
            className.push('highlight-red');
        }

        if (dose.dose_text_start != null && pos >= dose.dose_text_start && pos <= dose.dose_text_end) {
            className.push('highlight-orange');
        }

        if (strength.strength_text_start != null && pos >= strength.strength_text_start && pos <= strength.strength_text_end) {
            className.push('highlight-orange');
        }

        if (route.route_text_start != null && pos >= route.route_text_start && pos <= route.route_text_end) {
            className.push('highlight-yellow');
        }

        if (frequency.frequency_text_start != null && pos >= frequency.frequency_text_start && pos <= frequency.frequency_text_end) {
            className.push('highlight-green');
        }

        if (when.when_text_start != null && pos >= when.when_text_start && pos <= when.when_text_end) {
            className.push('highlight-green');
        }

        if (duration.duration_text_start != null && pos >= duration.duration_text_start && pos <= duration.duration_text_end) {
            className.push('highlight-green');
        }

        if (indication.indication_text_start != null && pos >= indication.indication_text_start && pos <= indication.indication_text_end) {
            className.push('highlight-purple');
        }

        className = className.join(' ');

        return className;
    }
    
    setSigComponents() {
        // keep in mind that these components could overlap...
        const sig_parsed = this.state.sig_parsed;
        const sig_parsed_components = {
            method: {
                method: sig_parsed.method,
                method_text: sig_parsed.method_text,
                method_text_start: sig_parsed.method_text_start,
                method_text_end: sig_parsed.method_text_end                
            },
            dose: {
                dose: sig_parsed.dose,
                dose_max: sig_parsed.dose_max,
                dose_unit: sig_parsed.dose_unit,
                dose_text: sig_parsed.dose_text,
                dose_text_start: sig_parsed.dose_text_start,
                dose_text_end: sig_parsed.dose_text_end
            },
            strength: {
                strength: sig_parsed.strength,
                strength_max: sig_parsed.strength_max,
                strength_unit: sig_parsed.strength_unit,
                strength_text: sig_parsed.strength_text,
                strength_text_start: sig_parsed.strength_text_start,
                strength_text_end: sig_parsed.strength_text_end
            },
            route: {
                route: sig_parsed.route,
                route_text: sig_parsed.route_text,
                route_text_start: sig_parsed.route_text_start,
                route_text_end: sig_parsed.route_text_end                
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
                when_text_end: sig_parsed.when_text_end
            },
            duration: {
                duration: sig_parsed.duration,
                duration_max: sig_parsed.duration_max,
                duration_unit: sig_parsed.duration_unit,
                duration_text: sig_parsed.duration_text,
                duration_text_start: sig_parsed.duration_text_start,
                duration_text_end: sig_parsed.duration_text_end
            },
            indication: {
                as_needed: sig_parsed.as_needed,
                indication: sig_parsed.indication,
                indication_text: sig_parsed.indication_text,
                indication_text_start: sig_parsed.indication_text_start,
                indication_text_end: sig_parsed.indication_text_end
            }      
        };
        this.setState({ sig_parsed_components });
    }


    render() {
        const { sig_parsed, sig_reviewed, sig_parsed_components } = this.state;
        return (
            <Row>
                <Col sm={12}>
                    <h3>
                    {sig_parsed_components && sig_parsed.sig_text.split('').map((c, p) => 
                        <span className={this.getClassName(p)}>{c}</span>
                    )}
                    </h3>
                </Col>
            </Row>
        );
    }
}

export { SigHighlighted }