import Header from '../components/Header';
import Footer from '../components/Footer';
import AutomaticEvaluationTable from '../components/AutomaticEvaluationTable';
import fetch from 'isomorphic-unfetch';

const Model = (props) => (
  <div>
    <Header />
    <main role="main" class="container">
      <h1 class="mt-5 font-weight-bold"> {props.model.name}</h1>
      <p class="lead">{props.model.description}</p>
      <div class="row">
        {props.evaluations.map(evaluation => <AutomaticEvaluationTable evaluation={evaluation}/>)}
      </div>

    </main>
    <Footer />
  </div>
);

Model.getInitialProps = async function(props) {
  const { query } = props;
  const modelRequest = await fetch('https://api.chateval.org/api/model?id=' + query.id);
  const modelData = await modelRequest.json();
  const evaluationRequest = await fetch('https://api.chateval.org/api/automatic_evaluations?model_id=' + query.id);
  const evaluationData = await evaluationRequest.json();
  return { model: modelData.model, evaluations: evaluationData.evaluations };
};

export default Model;