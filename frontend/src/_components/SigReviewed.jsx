import React from 'react';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup'
import ToggleButton from 'react-bootstrap/ToggleButton'

class SigReviewedOverall extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            sig_reviewed: this.props.sig_reviewed,
            sig_parsed: this.props.sig_parsed
        };
    }

    render() {
        const { sig_reviewed, sig_parsed } = this.state;
        return (
            <ToggleButtonGroup type="radio" name="sig_correct" defaultValue={sig_reviewed && sig_reviewed.sig_correct} onChange={this.props.handleChange}>
                <ToggleButton value={true} variant="light"><span className="material-icons">check_circle</span></ToggleButton>
                <ToggleButton value={false} variant="light"><span className="material-icons">cancel</span></ToggleButton>
            </ToggleButtonGroup>
        );
    }
}

class SigReviewedPart extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            sig_part: this.props.sig_part,
            sig_reviewed: this.props.sig_reviewed,
            sig_parsed: this.props.sig_parsed
        };
    }

    render() {
        const { sig_part, sig_reviewed, sig_parsed } = this.state;
        const name = sig_part + "_status";
        return (
            <div>
                {sig_reviewed &&
                    <ToggleButtonGroup type="radio" name={name} defaultValue={sig_reviewed && sig_reviewed[name]} onChange={this.props.handleChange}>
                            {sig_parsed[sig_part] &&
                                <ToggleButton value={0} variant="light"><span className="material-icons">cancel</span></ToggleButton>
                            }
                            {!sig_parsed[sig_part] &&
                                <ToggleButton value={1} variant="light"><span className="material-icons">help</span></ToggleButton>
                            }
                            <ToggleButton value={2} variant="light"><span className="material-icons">build_circle</span></ToggleButton>
                    </ToggleButtonGroup>
                }         
            </div>
        );
    }
}


/*
STATUS_CHOICES = [(0, 'incorrect'), (1, 'missing'), (2, 'optimize')]

class SigReviewed(models.Model):
    # foreign keys
    sig_parsed = models.OneToOneField(SigParsed, related_name='sig_reviewed', null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='sigs_reviewed', null=True, on_delete=models.SET_NULL)
   # time stamp
    created = models.DateTimeField(auto_now_add=True)
    # overall sig correct
    sig_correct = models.BooleanField(null=True)
    # status of individual sig components if overall sig not correct
    method_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    dose_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    strength_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    route_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    frequency_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    duration_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    indication_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    # theme
    themes = models.CharField(max_length=250, null=True)
    # additional notes
    notes = models.TextField(null=True)
*/

export { SigReviewedOverall, SigReviewedPart }