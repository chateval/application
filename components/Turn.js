const Turn = (props) => (
  <div class="col-md-6 vmargin">
    <div class="card">
      <div class="card-body">
        <h6 class="card-title mb-2 text-muted">{props.prompt.prompt_text}</h6>
        {props.responses.map(response => <div> <a class="badge badge-light font-weight-normal"> {response.name} </a> {response.response.response_text} </div> )}
      </div>
    </div>
  </div>
)
export default Turn;