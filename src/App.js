import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import TeamProfiles from './pages/TeamProfiles';
import Support from './pages/Support';
import Resources from './pages/Resources';
import Championship from './pages/Championship';
import SignUp from './pages/SignUp';
import SignIn from './pages/SignIn';
import TeamProfile from './pages/TeamProfile';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="container mx-auto px-4">
          <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/about" component={About} />
            <Route path="/team-profiles" component={TeamProfiles} />
            <Route path="/support" component={Support} />
            <Route path="/resources" component={Resources} />
            <Route path="/championship" component={Championship} />
            <Route path="/signup" component={SignUp} />
            <Route path="/signin" component={SignIn} />
            <Route path="/team-profile" component={TeamProfile} />
          </Switch>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;