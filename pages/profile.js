import Header from '../components/Header';
import Footer from '../components/Footer';

const Account = (props) => (
  <div>
    <Header />
    <main role="main" class="container">
      <h1 class="mt-5 font-weight-bold">Profile</h1>
      <p class="lead">A ChatEval account is required for uploading models. Creating an account is simple and 100% free for researchers. </p>
      <hr />
      <div class="row">
        <div class="col-md-6">
          <h2>Log In</h2>
          <form>
            <div class="form-group">
                <label for="exampleInputEmail1">Email address</label>
                <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
            </div>
            <div class="form-group">
                <label for="exampleInputPassword1">Password</label>
                <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password" />
            </div>
            <button type="submit" class="btn btn-primary">Enter</button>
          </form>
        </div>

        <div class="col-md-6">
          <h2>Sign Up</h2>
          <form>
          <label for="exampleInputEmail1">Researcher and Institution</label>

            <div class="row form-group">
              <div class="col">
                <input type="text" class="form-control" placeholder="Full Name" />
              </div>
              <div class="col">
                <input type="text" class="form-control" placeholder="Institution Name" />
              </div>
            </div>
            <div class="form-group">
                <label for="exampleInputEmail1">Email address</label>
                <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
            </div>
            <div class="form-group">
                <label for="exampleInputPassword1">Password</label>
                <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password" />
            </div>

            <div class="form-group">
                <label for="exampleInputPassword1">Confirm Password</label>
                <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password" />
            </div>
            <button type="submit" class="btn btn-primary">Create Account</button>
          </form>
        </div>
      </div>
    </main>
    <Footer />
  </div>
);

export default Account;