import React, { Component } from 'react';
import Modal from '../UI/Modal/Modal';
import NavigationItem from '../Navigation/NavigationItems/NavigationItem/NavigationItem';


class CreateChoiceModal extends Component {
  state = {
    showModal: true
  }

  handlerModalClosed = () => {
    this.setState({ showModal: false });
    this.props.history.goBack();
  }

  render() { 
    return (
      <div>
        <Modal show={this.state.showModal} modalClosed={this.handlerModalClosed}>
          <h4>Modal for choice what create</h4>
          <NavigationItem link="create/question">New Question</NavigationItem>
          <NavigationItem link="create/snippet">New Snippet</NavigationItem>
        </Modal>
      </div>
    )
  }
}
 
export default CreateChoiceModal;