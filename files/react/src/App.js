import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';
import './App.css';
IMPORTS_SECTION
/*import ComponentA from "./components/ComponentA";
import ComponentB from "./components/ComponentB.jb";*/

function App() {
  return (
      <Router>
          <Navbar bg="dark" variant="dark" expand="lg">
              <Container>
                  <Navbar.Brand as={Link} to="/">APP_NAME</Navbar.Brand>
                  <Navbar.Toggle aria-controls="basic-navbar-nav" />
                  <Navbar.Collapse id="basic-navbar-nav">
                      <Nav className="me-auto">
                          LINKS_SECTION
                          {/*<Nav.Link as={Link} to="/componentA">Component A</Nav.Link>
                          <Nav.Link as={Link} to="/componentB">Component B</Nav.Link>*/}
                      </Nav>
                  </Navbar.Collapse>
              </Container>
          </Navbar>

          <Container className="mt-4">
              <Routes>
                  ROUTE_SECTION
                  {/*<Route path="/componentA" element={<ComponentA />} />
                  <Route path="/componentB" element={<ComponentB />} />
                  <Route path="/" element={<h2>Welcome! Select a component.</h2>} />*/}
              </Routes>
          </Container>
      </Router>
  );
}

export default App;
