import { CSVLink } from "react-csv";

// returns CSV formatted array for each dataset's evaluation metrics
function getCSVArray(auto_evals) {
  let csv = [];
  for (const auto_eval of auto_evals) { csv.push([auto_eval.name, auto_eval.value]) };
  return csv;
}

const AutomaticEvaluationTable = (props) => (
  <div className="col-md-12">
    <h3 class="card-title"> {props.evaluation.evalset.long_name} </h3>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th scope="col">Measure</th>
          <th scope="col">Value</th>
        </tr>
      </thead>
      <tbody>
        {props.evaluation.auto_evals.map(auto_eval => 
          <tr>
            <td>{auto_eval.name}</td>
            <td>{auto_eval.value}</td>
          </tr>
        )}
      </tbody>
    </table>
    <CSVLink 
      data={getCSVArray(props.evaluation.auto_evals)}
      filename={props.evaluation.evalset.name + ".csv"}
    >
      Download CSV
  </CSVLink>
  </div>
);

export default AutomaticEvaluationTable;