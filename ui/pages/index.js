import Header from '../components/Header';
import Footer from '../components/Footer';

const Index = () => (
  <div>
    <Header />
    <main role="main" className="container">
      <h1 className="mt-5 font-weight-bold"> ChatEval</h1>
      <p className="lead">ChatEval is a scientific framework for evaluating <mark>open domain chatbots</mark>. 
      Researchers can submit their trained models to effortlessly receive comparisons with baselines and prior work. 
      Since all evaluation code is <mark>open source</mark>, we ensure evaluation is performed in a standardized and transparent way. 
      Additionally, open source baseline models and an ever growing groups public evaluation sets are available for public use.</p>
      <a href="https://my.chateval.org/upload" className="btn btn-primary">Upload Model</a>
      <br /> <br />
      <h5 className="card-title"> How much does ChatEval cost? </h5>
      <p className="card-text">ChatEval is currently <mark>free</mark> for academic researchers. It is actively developed by the NLP Group of the University of Pennyslvania.</p>
      <h5 className="card-title"> Is there an online demo video? </h5>
      <p className="card-text">You can find a video tutorial for ChatEval <a href="https://youtu.be/36rAoujxLAA">here</a>.</p>
      <h5 className="card-title"> How is automatic chatbot model assesment and evaluation performed? </h5>
      <p className="card-text">Read more about how automatic model assessment and evaluation is done <a href="/about">here</a>.</p>
      <h5 className="card-title"> How was ChatEval built? </h5>
      <p className="card-text">The ChatEval webapp is built using Django and React (front-end) using Magnitude word embeddings format for evaluation. Our source code is available on <a href="https://github.com/chateval">Github</a>.</p>
      <script src="https://widget.flow.ai/w/ZjExYWZmM2UtOWY4OS00NDQ4LTk2ZDUtZGE5N2RhOTNmYzUwfDBiNGY0MTE4LTRkM2MtNGMxOS1iNjYxLWQ1ZGY1Zjk5ZTJjOQ==/flow-webclient-1.1.2.min.js"></script>
    </main>
    <Footer />
  </div>
);

export default Index;
