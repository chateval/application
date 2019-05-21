import React, { Component } from 'react';
import fetch from 'isomorphic-unfetch';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Select from 'react-select'
import makeAnimated from 'react-select/lib/animated';
import AutomaticEvaluationTable from '../components/AutomaticEvaluationTable';

class Models extends Component {
  constructor(props) {
    super(props);
    this.state = { models: [] };
  }

   handleModelChange = async selections => {
    let models = [];

    for (const selection of selections) {
      const modelRequest = await fetch('https://api.chateval.org/api/model?id=' + selection.value);
      const modelData = await modelRequest.json();
      const evaluationRequest = await fetch('https://api.chateval.org/api/automatic_evaluations?model_id=' + selection.value);
      const evaluationData = await evaluationRequest.json();      
      models.push({ model: modelData.model, evaluations: evaluationData.evaluations });
    }

    this.setState({ models });
  }

  render() {
    return (
      <div>
        <Header />
        <main role="main" class="container">
          <h1 class="mt-5 font-weight-bold">Models</h1>
          <p>Compare multiple models at once.</p>
          <Select
            closeMenuOnSelect={false}
            components={makeAnimated()}
            isMulti
            placeholder="Select Models"
            options={this.props.options}
            onChange={this.handleModelChange}
          />    
          <div class="row">
            {this.state.models.map(model =>
              <div className="col-md-6">
                <br />
                <div className="card">
                  <div class="card-header">
                  <h3 class="card-title vmargin">{model.model.name}</h3>
                  </div>
                  <div class="card-body">
                    {model.evaluations.map(evaluation => 
                      <div>
                        <AutomaticEvaluationTable evaluation={evaluation} /> 
                      </div>
                    )} 
                  <a style={{paddingLeft: "0.8rem"}} href={"/model?id=" + model.model.model_id}>View Model</a>
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
        <Footer />
      </div>
    );
  }
}

Models.getInitialProps = async function() {
  let models = [];

  const modelRequest = await fetch('https://api.chateval.org/api/models');
  const modelData = await modelRequest.json();

  modelData.models.forEach(model => {
    models.push({ 'value': model.id, 'label': model.name})
  });

  return { options: models };
};

export default Models;