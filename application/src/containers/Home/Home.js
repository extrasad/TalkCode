import React, { Component } from 'react';
import Card from '../../components/UI/Card/Card';
import { Container, Row, Col } from 'react-grid-system';
import Line from '../../components/UI/Line/Line';
import HomeEditor from '../../components/HomeEditor/HomeEditor';
import classes from './Home.css';

import code from './Content/Code';


class HomeContainer extends Component {
  render() { 
    return (
      <React.Fragment>
        <Container fluid>
          <Row>
            <Col md={4}>
              <Card>
                Questions:
                <Line/>
                Follow more people for see questions..
              </Card>
            </Col>
            <Col md={4}>
              <Card>
                Answers:
                <Line/>
                Follow more people for see answers..
              </Card>
            </Col>
            <Col md={4}>
              <Card>
                Snippets:
                <Line/>
                Follow more people for see snippets..
              </Card>
            </Col>
          </Row>
        </Container>
        <Container fluid style={{marginTop: "2vw"}}>
          <Row>
            <Col md={6} style={{paddingLeft: "20px"}}>
              <Row>
                <Col md={12}>
                  <h4>Snippets</h4>
                  <p>Let others comment your snippets, receive stars for your coding skill and learn more</p>
                </Col>
                <Col md={12}>
                  <h4>Questions</h4>
                  <p>Solve your intrigues, asking about anything about code</p>
                </Col>
                <Col md={12}>
                  <h4>Answers</h4>
                  <p>Help others by answering questions</p>
                </Col>
              </Row>
            </Col>
            <Col md={6} className={classes.ColEditor}>
              <HomeEditor value={code}/>
            </Col>
          </Row>
        </Container>
      </React.Fragment>
    )
  }
}
 
export default HomeContainer;