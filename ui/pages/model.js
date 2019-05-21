import React, { Component } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import TurnList from '../components/TurnList';
import AutomaticEvaluationTable from '../components/AutomaticEvaluationTable';
import fetch from 'isomorphic-unfetch';
import Select from 'react-select';
import Chart from 'react-google-charts';

class Model extends Component {
  constructor(props) {
    super(props);
    this.state = { models: [], prompts: [], responses: [] };
    this.handleEvaluationDatasetChange.bind(this);
  }

  handleEvaluationDatasetChange = async(evalset) => {
    const promptsRequest = await fetch('http://localhost:8000/api/prompts?evalset=' + evalset.value);
    const promptsData = await promptsRequest.json();
    const prompts = promptsData.prompts.slice(0, 200);

    const requestURL = 'http://localhost:8000/api/responses?evalset=' + evalset.value + "&model_id=" + this.props.model.id
    const responsesRequest = await fetch(requestURL);
    const responsesData = await responsesRequest.json();
    const responses = [{ model_id: this.props.model.id, responses: responsesData.responses.slice(0, 200), name: this.props.model.name }];

    console.log(prompts, responses)

    this.setState({ prompts });
    this.setState({ responses });
  }

  render() {
    return (
      <div>
        <Header />
        <main role="main" class="container">
          <h1 class="mt-5 font-weight-bold"> {this.props.model.name}</h1>
          <p class="lead">{this.props.model.description}</p>
          <hr />
          <h2 class="font-weight-bold">Automatic Evaluations</h2>
          <div class="row">
            {this.props.evaluations.map(evaluation => <AutomaticEvaluationTable evaluation={evaluation}/>)}
          </div>
          <hr />
          <h2 class="font-weight-bold">Human Evaluations</h2>
          <Chart
            width={'800px'}
            height={'300px'}
            chartType="BarChart"
            loader={<div>Loading Chart</div>}
            data={[
              ['City', this.props.model.name + "wins", 'Competing Model wins', 'Tie'],
              ['New York City, NY', 8175000, 8008000, 0],
              ['Los Angeles, CA', 3792000, 3694000, 0],
              ['Chicago, IL', 2695000, 2896000, 0],
              ['Houston, TX', 2099000, 1953000, 0],
              ['Philadelphia, PA', 1526000, 1517000, 0],
            ]}
            options={{
              title: 'A/B Comparisons',
              chartArea: { width: '50%' },
              isStacked: true,
              hAxis: {
                title: 'Number of Turns',
                minValue: 0,
              },
              vAxis: {
                title: 'Competing Model',
              },
            }}
            // For tests
            rootProps={{ 'data-testid': '3' }}
          />
          <hr />
          <h2 class="font-weight-bold">Conversations</h2>
          <Select 
            options={this.props.evalsets} 
            className="vmargin"
            placeholder="Select Evaluation Dataset"
            onChange={this.handleEvaluationDatasetChange}
          />
          <TurnList prompts={this.state.prompts} responses={this.state.responses} />
        </main>
        <Footer />
      </div>
    );
  }
}

Model.getInitialProps = async function(props) {
  const { query } = props;
  const modelRequest = await fetch('http://localhost:8000/api/model?id=' + query.id);
  const modelData = await modelRequest.json();
  const evaluationRequest = await fetch('https://api.chateval.org/api/automatic_evaluations?model_id=' + query.id);
  const evaluationData = await evaluationRequest.json();
  let evalsets = [];
  modelData.model.evalsets.forEach(evalset => {
    evalsets.push({ 'value': evalset.evalset_id, 'label': evalset.name})
  });
  return { evalsets, model: modelData.model, evaluations: evaluationData.evaluations };
};

export default Model;