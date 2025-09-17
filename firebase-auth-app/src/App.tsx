import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import SignInPage from './pages/SignInPage';
import SignUpPage from './pages/SignUpPage';

const App: React.FC = () => {
  return (
    <Router>
      <Switch>
        <Route path="/signin" component={SignInPage} />
        <Route path="/signup" component={SignUpPage} />
        <Route path="/" exact>
          <h1>Welcome to the Authentication App</h1>
        </Route>
      </Switch>
    </Router>
  );
};

export default App;