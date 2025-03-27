import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';
import './App.css';
IMPORTS_SECTION

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
                      </Nav>
                  </Navbar.Collapse>
              </Container>
          </Navbar>

          <Container className="mt-4">
              <Routes>
                  ROUTE_SECTION
              </Routes>
          </Container>
      </Router>
  );
}

export default App;
