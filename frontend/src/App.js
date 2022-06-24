import React from 'react';

import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

import { PrivateRoute, Header, Footer } from './_components';
import { HomePage } from './HomePage';
import { LoginPage } from './LoginPage';
import { LogoutPage } from './LogoutPage';
import { SigPage } from './SigPage';
import { DocsPage } from './DocsPage';
import { TermsOfServicePage } from './TermsOfServicePage';
import { DisclaimerPage } from './DisclaimerPage';
import { PrivacyPolicyPage } from './PrivacyPolicyPage';
import { DemoPage } from './DemoPage';

import './App.css';
/* NOTE: replace the last Route (which currently points to HomePage duplicate) with a NotFoundComponent for 404s */

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
        isLoggedIn: false
    };
  }

  componentDidMount() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
      this.setState({ 
        isLoggedIn: true,
      });
    }
    window.scrollTo(0, 0);    
  }

  login(username, password) {
    return userService.login(username, password)
    .then(
      user => {
        this.setState({isLoggedIn: true});
        return user;
      }
    );
  }

  logout(username, password) {
    return userService.logout()
    .then(
      user => {
        this.setState({isLoggedIn: false});
        return user;
      }
    );
  }

  render() {
    const { isLoggedIn } = this.state;
    return (
        <div>
            <Router>
              <Header isLoggedIn={this.state.isLoggedIn} />
                <Switch>
                  <Route path="/login" component={LoginPage} />
                  <Route path="/logout" component={LogoutPage} />
                  <PrivateRoute exact path="/sig" component={SigPage} />
                  <PrivateRoute exact path="/demo" component={DemoPage} />
                  <Route path="/docs" component={DocsPage} />
                  <Route path="/terms-of-service" component={TermsOfServicePage} />
                  <Route path="/disclaimer" component={DisclaimerPage} />
                  <Route path="/privacy-policy" component={PrivacyPolicyPage} />
                  <Route path="/" component={HomePage} />
                  <Route component={HomePage} />
                </Switch>
            <Footer isLoggedIn={isLoggedIn} />
          </Router>
      </div>
    );
  }
}

export default App;
