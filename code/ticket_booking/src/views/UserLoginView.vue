<template>
    <!-- include the navbar component here-->
    <NavBarComponent :page_title="page_title" />
    <br /><br />
    <br /><br />
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-4">
          <div class="login">
            <h2>Welcome, Please Login</h2>
            <br />
            <p id="error" style="color: red;"></p>
            <form @submit.prevent="login">
              <div class="form-group">
                <label for="username">Username:</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  placeholder="Enter username"
                  name="username"
                />
              </div>
              <div class="form-group">
                <label for="password">Password:</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  placeholder="Enter password"
                  name="password"
                />
              </div>
              <button type="submit" class="btn btn-primary">Login</button>
            </form>
            <br />
            <p>Not registered? <router-link to="/user_signup">Sign Up</router-link></p>
            <br /><br /><br />
            <p id="admin-ask-text">
                Are you an admin? <router-link to="/admin_login">Admin Login</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import NavBarComponent from '../components/NavBarComponent.vue';


export default {
    name: 'UserLogin',
    components: {
        NavBarComponent
    },
    data() {
        return {
            page_title: 'My Movie Manager'
        }
    },
    methods: {
        login: async function() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;            

    const response = await fetch('http://127.0.0.1:5000/api/user_login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    }).catch(error => document.getElementById('error').innerText = 'Something went wrong. Please try again. The error is: ' + error);

    const responseData = await response.json();

    if (responseData.login === true && responseData.token) {
        localStorage.setItem('user_token', responseData.token);
        localStorage.setItem('user_id', responseData.token_payload.user_id);

        // Redirect to the dashboard
        this.$router.push('/user_dashboard');
    } else {
        document.getElementById('error').innerText = 'Invalid username or password.';
    }
}

    }
}


</script>

<style>
#admin-ask-text {
    text-align: center;
}

.login {
    justify-content: center;
    align-items: center;
    height: 100vh;
    max-width: 500px;
  }
  
  
  .form-group {
    margin-bottom: 20px;
    margin-top: 20px;

  }

</style>
  


