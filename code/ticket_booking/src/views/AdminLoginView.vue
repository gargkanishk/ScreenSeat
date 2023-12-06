<template>
    <div>
      <br /><br />
      <div class="container login col-md-4">
        <h2>Admin Login</h2> 
        <br />
        <p id="error" style="color: red;"></p>
        <form @submit.prevent="submitAdminLogin">
          <div class="form-group">
            <label for="username">Username:</label>
            <input
              type="text"
              class="form-control"
              id="username"
              placeholder="Enter username"
              v-model="username"
            />
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input
              type="password"
              class="form-control"
              id="password"
              placeholder="Enter password"
              v-model="password"
            />
          </div>
          <button type="submit" class="btn btn-primary">Login</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminLogin',
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async submitAdminLogin() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;            

    const response = await fetch('http://127.0.0.1:5000/api/admin_login', {
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

        this.$router.push('/admin_dashboard');
    } else {
        document.getElementById('error').innerText = 'Invalid username or password.';
    }
}
    },
  };
  </script>
  
  <style>
  .login {
    justify-content: center;
    align-items: center;
    height: 100vh;
    max-width: 500px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  </style>
  