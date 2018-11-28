const Card = (props) => (
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">{props.title}</h5>
      <h6 class="card-subtitle mb-2 text-muted">{props.subtitle}</h6>
      <p class="card-text">{props.description}</p>
      <a href={props.url} class="btn btn-sm btn-primary">{props.link}</a>
    </div>
  </div>
);
      
export default Card;