import Header from '../components/Header';
import Footer from '../components/Footer';
import Card from '../components/Card';
import fetch from 'isomorphic-unfetch';

const About = (props) => (
  <div>
    <Header />
    <main role="main" class="container">
      <h1 class="mt-5 font-weight-bold">About Evaluation</h1>
      <p class="lead">Model responses are generated using an evaluation dataset of prompts and then uploaded to ChatEval. The responses are then 
      evaluated using a series of automatic evaluation metrics, and are compared against selected baseline/ground truth models (e.g. humans). </p>

      <h2 class="mt-4 font-weight-bold">Evaluation Datasets</h2>
      <p>ChatEval offers evaluation datasets consisting of prompts that uploaded chatbots are to respond to. Evaluation datasets are available
        to download for free and have corresponding baseline models. </p>
      <div class="row">
        {props.evalsets.map(evalset => 
          <div className="col-md-6">
            <Card title={evalset.long_name} subtitle={"Supported ChatEval Dataset"} description={evalset.description} link={"Download Dataset"} url={evalset.source} />
            <br />
          </div>
        )}
      </div>

      <h2 class="mt-4 font-weight-bold">ChatEval Baselines</h2>
      <p>
        ChatEval offers "ground-truth" baselines to compare uploaded models with. Baseline models range from human responders to established chatbot models.
        Baselines are handpicked and uploaded by the ChatEval Team.
      </p>
      <div class="row"> 
        {props.baselines.map(baseline => 
          <div className="col-md-4">
            <Card title={baseline.name} url={"/model?id="+baseline.model_id} link={"View Model"} subtitle={baseline.description} />
            <br />
          </div>
        )}
      </div>

      <h2 class="mt-4 font-weight-bold">Automated Evaluation Methods</h2>
      <p> The ChatEval Platform handles certain automated evaluations of chatbot responses. These metrics are documented <a href="https://github.com/chateval/evaluation">here</a>. 
      Models can be ranked according to a specific metric and viewed as a leaderboard.</p>
      <div class="row">
        {props.metrics.map(metric => 
          <div className="col-md-3">
            <Card title={metric.name} subtitle={"Metric"} description={metric.info} link={"View Source"} url={"https://raw.githubusercontent.com/chateval/evaluation/master/auto_eval_utils.py"} />
            <br />
          </div>
        )}
      </div>
      <h1 className="mt-5 font-weight-bold">References</h1>
      <p>
        Higashinaka, Ryuichiro, Kotaro Funakoshi, Yuka Kobayashi, and Michimasa Inaba. "The dialogue breakdown detection challenge: Task description, datasets, and evaluation metrics." In <i>LREC</i>. 2016.
      </p>
      <p>
        Liu, Chia-Wei, Ryan Lowe, Iulian Serban, Mike Noseworthy,Laurent Charlin, and Joelle Pineau. "How not to evaluate your dialogue system: An empirical study of unsupervised evaluation metrics for dialogue response generation." In <i>EMNLP</i>, pp. 2122–2132. Association for Computational Linguistics,  2016.
      </p>
      <p>
        Forgues, Gabriel, Joelle Pineau, Jean-Marie Larchevêque, and Réal Tremblay. "Bootstrapping dialog systems with word embeddings." In <i>NIPS, modern machine learning and natural language processing workshop</i>, vol. 2. 2014.
      </p>
      <p>
        Papineni, Kishore, Salim Roukos, Todd Ward, and Wei-Jing Zhu. "BLEU: a method for automatic evaluation of machine translation." In <i>Proceedings of the 40th annual meeting on association for computational linguistics</i>, pp. 311-318. Association for Computational Linguistics, 2002.
      </p>
      <p>
        Rus, Vasile, and Mihai Lintean. "A comparison of greedy and optimal assessment of natural language student input using word-to-word similarity metrics." In <i>Proceedings of the Seventh Workshop on Building Educational Applications Using NLP</i>, pp. 157-162. Association for Computational Linguistics, 2012.
      </p>
      <p>
        Tiedemann, Jörg. "News from OPUS-A collection of multilingual parallel corpora with tools and interfaces." In Recent advances in natural language processing, vol. 5, pp. 237-248. 2009.
      </p>
      <p>
        Vinyals, Oriol, and Quoc Le. "A neural conversational model." arXiv preprint arXiv:1506.05869 (2015).
      </p>
    </main>
    <Footer />
  </div>
);

About.getInitialProps = async function() {
  let data = {};
  const baselineRequest = await fetch('https://api.chateval.org/api/baselines');
  const baselineData = await baselineRequest.json();
  data.baselines = baselineData.baselines;

  const evalsetRequest = await fetch('https://api.chateval.org/api/evaluationdatasets');
  const evalsetData = await evalsetRequest.json();
  data.evalsets = evalsetData.evaluationdatasets;

  const metricRequest = await fetch('https://api.chateval.org/api/metrics');
  const metricData = await metricRequest.json();
  data.metrics = metricData.metrics;

  return data;
};

export default About;