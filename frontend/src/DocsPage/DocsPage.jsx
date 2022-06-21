import React from 'react';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

class DocsPage extends React.Component {
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
                        <h1>API Documentation</h1>
                        <div className="stackedit__html">
                            <p>
                                Before getting started,{" "}
                                <a href="mailto:hello@parserx.io">request an API key</a>. Please review our{" "}
                                <a href="https://parserx.io/terms-of-service">Terms Of Service</a> before deploying API
                                integration to avoid any unexpected account issues.
                            </p>
                            <h2 id="request-authentication">Request Authentication</h2>
                            <p>All requests must have an API key.</p>
                            <p>
                                <strong>To authenticate:</strong>
                                <br />
                                Headers of your request must include:
                            </p>
                            <p>
                                <code>Authorization: Api-Key &lt;your API key here&gt;</code>
                                <br />
                                <code>Content-Type: application/json</code>
                            </p>
                            <p>
                                Invalid API keys will result in an <code>HTTP 401, Unauthorized</code>{" "}
                                error.
                            </p>
                            <h2 id="api-resources">API Resources</h2>
                            <p>
                                The ParseRx API expects HTTP URL request parameters and returns JSON
                                responses. All requests must include your API key.
                            </p>
                            <table>
                                <thead>
                                <tr>
                                    <th align="left">Request</th>
                                    <th />
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <td align="left">
                                    POST <strong>/sig/</strong>
                                    </td>
                                    <td>
                                    Generate / return a parsed sig and information on review status.
                                    </td>
                                </tr>
                                <tr>
                                    <td align="left">URL</td>
                                    <td>
                                    <a href="https://api.parserx.io/sig/">https://api.parserx.io/sig/</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="left">Format</td>
                                    <td>JSON</td>
                                </tr>
                                <tr>
                                    <td align="left">Body</td>
                                    <td>
                                    <code>
                                        {"{"} <br/>
                                            "sig_text": "tk 1-2 tab po qid x10d prn pain", (REQUIRED) string - your sig text here<br/>
                                            "ndc": "12345678911", (optional) numeric ndc11 string - if you want to infer sig elements by ndc<br/>
                                            "rxcui": "123456" (optional) numeric rxcui string - if you want to infer sig elements by rxcui<br/>
                                        {"}"}
                                    </code>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            <p>
                                <strong>NOTE:</strong> Depending on whether you submit a sig that ParseRx
                                has parsed before, you will receive two different server responses.
                            </p>
                            <ul>
                                <li>
                                <code>HTTP 200, OK</code> - ParseRx has parsed this sig before, so it is
                                just returning that previously parsed sig from the database.
                                </li>
                                <li>
                                <code>HTTP 201, Created</code> - ParseRx has not parsed this sig before,
                                so it is dynamically parsing it, saving it to the database, and returning
                                the result.
                                </li>
                            </ul>
                            <p>
                                <strong>Response</strong>
                            </p>
                            <p>
                                <code>sig_text</code>
                            </p>
                            <ul>
                                <li>
                                A string containing the original <code>sig_text</code> from the request,
                                converted to lower case, and duplicate spaces converted to single spaces.
                                </li>
                            </ul>
                            <p>
                                <code>sig_parsed</code>
                            </p>
                            <ul>
                                <li>
                                A JSON object containing all the parsed components of the free text sig.
                                See details of each component below.
                                </li>
                            </ul>
                            <p>
                                <code>sig_inferred</code>
                            </p>
                            <ul>
                                <li>
                                A JSON object containing all the inferred sig components if the request included
                                an <code>ndc</code> or <code>rxcui</code> parameter.
                                See details of each component below.
                                </li>
                                <li>
                                This entire object will only appear if a valid <code>ndc</code> or <code>rxcui</code> are included
                                as a request parameter.  If both are included, <code>ndc</code> will take precedence over <code>rxcui</code>.
                                </li>
                            </ul>
                            <p>
                                <strong>Parsed sig components</strong>
                            </p>
                            <p>
                                <code>method</code>
                            </p>
                            <ul>
                                <li>How the medication is administered (i.e. take, inject, inhale).</li>
                            </ul>
                            <p>
                                <code>dose</code>
                                <br />
                                <code>dose_max</code>
                                <br />
                                <code>dose_unit</code>
                            </p>
                            <ul>
                                <li>
                                How much medication patient is instructed to take based on dosage (i.e. 2
                                tablets, 30 units, 1-2 puffs).
                                </li>
                                <li>
                                Numbers represented as words in the sig will be converted to integers
                                (i.e. “one” will be converted to 1).
                                </li>
                            </ul>
                            <p>
                                <code>strength</code>
                                <br />
                                <code>strength_max</code>
                                <br />
                                <code>strength_unit</code>
                            </p>
                            <ul>
                                <li>
                                How much medication the patient is instructed to take based on strength
                                (i.e. 500 mg, 15 mL, 17 g).
                                </li>
                                <li>
                                <strong>NOTE:</strong> ParseRx intentionally does not parse multiple
                                ingredient strengths (i.e. if 5/325 mg is in a sig, it will return{" "}
                                <code>null</code> for <code>strength</code>).
                                </li>
                            </ul>
                            <p>
                                <code>route</code>
                            </p>
                            <ul>
                                <li>
                                Route of administration of the medication (i.e. by mouth, via inhalation,
                                in left eye).
                                </li>
                            </ul>
                            <p>
                                <code>frequency</code>
                                <br />
                                <code>frequency_max</code>
                                <br />
                                <code>period</code>
                                <br />
                                <code>period_max</code>
                                <br />
                                <code>period_unit</code>
                                <br />
                                <code>time_duration</code>
                                <br />
                                <code>time_duration_unit</code>
                                <br />
                                <code>day_of_week</code>
                                <br />
                                <code>time_of_day</code>
                                <br />
                                <code>when</code>
                                <br />
                                <code>offset</code>
                                <br />
                                <code>bounds</code>
                                <br />
                                <code>count</code>
                                <br />
                                <code>frequency_readable</code>
                            </p>
                            <ul>
                                <li>
                                How often medication should be administered (i.e. every 4-6 hours, three
                                times daily, once daily in the morning with meal).
                                </li>
                                <li>
                                Due to the complexity and variety of medication instructions, these
                                elements are based off of an existing standard -{" "}
                                <a href="https://www.hl7.org/fhir/datatypes.html#Timing">FHIR Timing</a>.
                                </li>
                                <li>
                                For convenience, a <code>frequency_readable</code> is generated to
                                represent a human-readable representation of the sig frequency.
                                </li>
                            </ul>
                            <p>
                                <code>duration</code>
                                <br />
                                <code>duration_max</code>
                                <br />
                                <code>duration_unit</code>
                            </p>
                            <ul>
                                <li>
                                How long the patient is instructed to take the medication (i.e. for 7
                                days, for 7-10 days, for 28 days).
                                </li>
                                <li>
                                <strong>NOTE:</strong> this is different from days’ supply, which
                                represents how long a given supply of medication should last.
                                </li>
                            </ul>
                            <p>
                                <code>as_needed</code>
                                <br />
                                <code>indication</code>
                            </p>
                            <ul>
                                <li>
                                Whether the medication should be taken “as needed” (i.e. PRN), and the
                                specific reason the patient is taking the medication (i.e. for pain, for
                                wheezing and shortness of breath, for insomnia).
                                </li>
                                <li>
                                <strong>NOTE:</strong> <code>indication</code> may be populated even if{" "}
                                <code>as_needed</code> is <code>false</code>. There are chronic
                                indications represented in sigs as well (i.e. for cholesterol, for high
                                blood pressure, for diabetes).
                                </li>
                            </ul>
                            <p>
                                <code>sig_reviewed_status</code>
                            </p>
                            <ul>
                                <li>
                                This is an indicator that a pharmacist / pharmacy resident has reviewed
                                the sig.
                                </li>
                                <li>
                                Depending on the review status of the sig, it will return either{" "}
                                <code>unreviewed</code>, <code>correct</code>, <code>incorrect</code>, or{" "}
                                <code>unknown</code>.
                                </li>
                            </ul>
                            <p>
                                <code>sig_reviewed</code>
                            </p>
                            <ul>
                                <li>
                                If <code>sig_reviewed_status</code> is <code>unreviewed</code> or{" "}
                                <code>unknown</code>, this will be <code>null</code>.
                                </li>
                                <li>
                                Otherwise, this will return an object containing the reviewed components
                                of the parsed sig. See details of each component below.
                                </li>
                            </ul>
                            <p>
                                <strong>NOTE:</strong> ParseRx will be constantly improving, and as such,
                                there may be multiple different versions of parsing a given sig. Each of
                                these parsing versions will be reviewed by a pharmacist or pharmacy resident
                                in time. If there exists a version that has a{" "}
                                <code>sig_reviewed_status</code> of <code>correct</code>, this is the
                                version that will be returned. Otherwise, the most recently parsed version
                                of the sig will be returned.
                            </p>
                            <p>
                                <strong>IMPORTANT:</strong> Pay close attention to the{" "}
                                <code>sig_reviewed_status</code> and <code>sig_reviewed</code> object. It is
                                your responsibility to use this information safely.
                            </p>
                            <p>
                                <strong>Reviewed sig components</strong>
                            </p>
                            <p>
                                <code>sig_correct</code>
                            </p>
                            <ul>
                                <li>
                                Whether the sig is considered to be parsed correctly overall or not.
                                </li>
                            </ul>
                            <p>
                                <code>method_status</code>
                                <br />
                                <code>dose_status</code>
                                <br />
                                <code>strength_status</code>
                                <br />
                                <code>route_status</code>
                                <br />
                                <code>frequency_status</code>
                                <br />
                                <code>duration_status</code>
                                <br />
                                <code>indication_status</code>
                            </p>
                            <ul>
                                <li>
                                If the sig is not considered to be parsed correctly overall, there may be
                                values in these fields representing what the specific issue(s) are.
                                <br />
                                – 0 = incorrect - ParseRx returned something for this component, but it
                                was not correct
                                <br />
                                – 1 = missing - ParseRx did not return anything for this component, when
                                it should have
                                <br />– 2 = optimize - ParseRx returned something for this component, but
                                it could be improved
                                </li>
                            </ul>
                            <p>
                                <strong>Inferred sig components</strong>
                            </p>
                            <p>
                                <code>method</code>
                                <br/>
                                <code>dose_unit</code>
                                <br/>
                                <code>route</code>
                            </p>
                            <ul>
                                <li>
                                This entire object will only appear if a valid <code>ndc</code> or <code>rxcui</code> are included
                                as a request parameter.  If both are included, <code>ndc</code> will take precedence over <code>rxcui</code>.
                                </li>
                                <li>
                                Any or all of the inferred sig components may be null if it is not possible to infer them.
                                </li>
                            </ul>

                            <h2 id="curl-example">Curl Example</h2>
                            <p>
                                <strong>Request</strong>
                                <br />
                                <code>
                                curl -d '{"{"}"sig_text":"take 1-2 tablets (100-200mg) po qid x7-10d prn
                                moderate pain"{"}"}' -H "Content-Type: application/json" -H
                                "Authorization: Api-Key &lt;your API key here&gt;" -X POST
                                https://api.parserx.io/sig/
                                </code>
                            </p>
                            <p>
                                <strong>Response</strong>
                                <br />
                                <code>HTTP 201, Created</code>
                            </p>
                            <pre className=" language-javascript">
                                <code className="prism  language-javascript">
                                <span className="token punctuation">{"{"}</span>
                                {"\n"}
                                <span className="token string">"id"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">14076</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                <span className="token string">"sig_text"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">
                                    "take 1-2 tablets (100-200mg) po qid x7-10d prn moderate pain"
                                </span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                <span className="token string">"sig_parsed"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token punctuation">{"{"}</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"id"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">16159</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"sig_text"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">
                                    "take 1-2 tablets (100-200mg) po qid x7-10d prn moderate pain"
                                </span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"created"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"2020-07-21T11:09:03.675359Z"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"version"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">0</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"method"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"take"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"dose"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"1"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"dose_max"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"2"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"dose_unit"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"tablet"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"strength"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"100"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"strength_max"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"200"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"strength_unit"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"mg"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"route"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"by mouth"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"frequency"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">4</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"frequency_max"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"period"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">1</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"period_max"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"period_unit"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"day"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"time_duration"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"time_duration_unit"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"day_of_week"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"time_of_day"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"when"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"offset"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"bounds"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"count"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"frequency_readable"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"4 times per day"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"duration"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">7</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"duration_max"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">10</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"duration_unit"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"day"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"as_needed"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token boolean">true</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"indication"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"moderate pain"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"sig_reviewed"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token keyword">null</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"sig_reviewed_status"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"unreviewed"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"method_text"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"take"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"method_text_start"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">0</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"method_text_end"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">4</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"dose_text"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">" 1-2 tablets"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"dose_text_start"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">4</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"dose_text_end"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">16</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"strength_text"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">" (100-200mg"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"strength_text_start"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">16</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"strength_text_end"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">27</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"route_text"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"po"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"route_text_start"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">29</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"route_text_end"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">31</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"frequency_text"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"qid"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"frequency_text_start"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">32</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"frequency_text_end"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">35</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"duration_text"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"7-10 d"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"duration_text_start"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">36</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"duration_text_end"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">42</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"indication_text"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token string">"prn moderate pain"</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"indication_text_start"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">43</span>
                                <span className="token punctuation">,</span>
                                {"\n"}
                                {"  "}
                                <span className="token string">"indication_text_end"</span>
                                <span className="token punctuation">:</span>{" "}
                                <span className="token number">60</span>
                                {"\n"}
                                {"  "}
                                <span className="token punctuation">{"}"}</span>
                                {"\n"}
                                <span className="token punctuation">{"}"}</span>
                                {"\n"}
                                </code>
                            </pre>
                            </div>



                    </Col>
                </Row>
            </Container>
        );
    }
}

export { DocsPage }; 