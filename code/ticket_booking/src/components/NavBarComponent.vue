<template>
    <nav v-if="page_title !== 'My Movie Manager'" class="navbar navbar-expand-md navbar-dark bg-dark">
      <div class="container">
        <router-link v-if="page_title !== 'My Movie Manager'" class="navbar-brand" :to="page_title !== 'Home' ? '/' : '/user_dashboard'">{{ page_title }}</router-link>
  
        <div v-if="showNavbar" class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav ml-auto">
            <li v-if="!isAdmin" class="nav-item">
              <router-link class="nav-link" to="/user_dashboard">Home</router-link>
            </li>
            <li v-if= "!isAdmin" class="nav-item">
              <router-link class="nav-link" to="/search">Search</router-link>
            </li>
            <li v-if="!isAdmin" class="nav-item">
              <router-link class="nav-link" to="/my_bookings">My Bookings</router-link>
            </li>
            <li v-if="isAdmin" class="nav-item">
              <router-link class="nav-link" to="/summary">Summary</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" @click="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    props: {
      page_title: {
        type: String,
        required: true,
      },
      isAdmin: {
        type: Boolean,
        required: false,
        default: false,
      },
    },
    data() {
      return {
        showNavbar: true,
      };
    },
    mounted() {
        if (this.page_title === 'My Movie Manager') {
            this.showNavbar = false;
        } 
    },
    methods: {
      
        logout() {
            localStorage.removeItem('token');
            this.$router.push('/');

            //alert the user that they have been logged out
            alert('You have been logged out');
        },
    },
  };
  </script>
  
  <style>
  /* Your component's styles go here */
  </style>
  