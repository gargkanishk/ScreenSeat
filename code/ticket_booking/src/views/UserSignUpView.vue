<template>
    <!-- include the navbar component here-->
    <NavBarComponent :page_title="page_title" />
    <br /><br />
    <br /><br />
    <div class="container signup col-md-4">
      <h2>Sign Up</h2>
      <form @submit.prevent="signup">
        <div class="form-group">
          <label for="username">Username:</label>
          <input
            type="text"
            class="form-control"
            id="username"
            placeholder="Enter username"
            v-model="username"
            required
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
            required
          />
        </div>
        <div class="form-group">
          <label for="confirm_password">Confirm Password:</label>
          <input
            type="password"
            class="form-control"
            id="confirm_password"
            placeholder="Confirm password"
            v-model="confirmPassword"
            required
          />
        </div>
  
        <button type="submit" class="btn btn-primary">Sign Up</button>
      </form>
      <br />
      <p>
        Already registered? <router-link to="/user_login">Login</router-link>
      </p>
    </div>
  </template>
  
  <script>
  import NavBarComponent from '../components/NavBarComponent.vue';
  
  export default {
    name: 'UserSignUp',
    components: {
      NavBarComponent,
    },
    data() {
      return {
        page_title: 'Sign Up',
        username: '',
        password: '',
        confirmPassword: '',
      };
    },
    methods: {
      signup: async function () {
        const signupData = {
          username: this.username,
          password: this.password,
        };

         const response = await fetch('http://127.0.0.1:5000/api/user_signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(signupData)
        });

        const responseData = await response.json();

        if (responseData['signup'] === true) {
            console.log('User signed up successfully.');
            this.$router.push('/');

            //notify the user
            alert('Your signup was successful, please login to continue.');
        } else {
            // show an error message
            alert(responseData.message);
        }


        console.log('Sign up form submitted.');
        console.log('Username:', this.username);
        console.log('Password:', this.password);
        console.log('Confirm Password:', this.confirmPassword);

      },
    },
  };
  </script>
  
  <style>
  .signup {
    justify-content: center;
    align-items: center;
    height: 100vh;
    max-width: 500px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  </style>
  