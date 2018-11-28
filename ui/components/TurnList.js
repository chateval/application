import React, { Component } from 'react';
import Turn from './Turn.js';

class TurnList extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let turns = [];

    for (let i = 0; i < this.props.prompts.length; i += 1) {
      let turn = { prompt: this.props.prompts[i], responses: [] };
      
      for (const model_response of this.props.responses) {
        let response = {};
        response.response = model_response.responses[i];
        response.name = model_response.name;
        response.model_id = model_response.model_id;

        turn.responses.push(response);
      }

      turns.push(turn);
    }

    return(
      <div className="row">
        {turns.map(turn => <Turn prompt={turn.prompt} responses={turn.responses}/>)}
      </div>
    );
  }
}

export default TurnList;