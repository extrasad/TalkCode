import React, { Component } from 'react';
import { Container, Row, Col } from 'react-grid-system';

import Line from '../../components/UI/Line/Line';

class ProfileContainer extends Component {
  render() { 
    return (
      <React.Fragment>
        <Container fluid>
          <Row>
            <Col>
              Username
            </Col>
          </Row>
        </Container>
      </React.Fragment>
    )
  }
}
 
export default ProfileContainer;