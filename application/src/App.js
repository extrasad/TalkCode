import React, { Component } from 'react';
import { Route, Switch, withRouter, Redirect } from 'react-router-dom';

import Layout from './hoc/Layout/Layout';
import AuthContainer from './containers/Auth/Auth';
import CreateChoiceModal from './components/CreateChoiceModal/CreateChoiceModal';
import Logout from './containers/Auth/Logout/Logout';
import CreateSnippet from './containers/CreateSnippet/CreateSnippet';
import QuestionContainer from './containers/Question/Question';
import CreateQuestionContainer from './containers/CreateQuestion/CreateQuestion';
import SnippetContainer from './containers/Snippet/Snippet';
import ProfileContainer from './containers/Profile/Profile';
import HomeContainer from './containers/Home/Home';


class App extends Component {
  render () {
    return (
      <div>
        <Layout> 
          <Switch>
            <Route path="/auth" component={AuthContainer} />
            <Route path="/create/snippet" component={CreateSnippet} />
            <Route path="/create/question" component={CreateQuestionContainer} />
            <Route path="/new" component={CreateChoiceModal} />
            <Route path="/logout" component={Logout} />
            <Route path="/question" component={QuestionContainer} />
            <Route path="/snippet" component={SnippetContainer} />
            <Route path="/profile" component={ProfileContainer} />
            <Route path="/" exact component={HomeContainer} />
            <Redirect to="/" />
          </Switch>
        </Layout>
      </div>
    );
  }
}

export default withRouter(App)