<template>
    <!-- Add the navbar and pass the page title and isAdmin -->
    <!-- <NavBarComponent :page_title="page_title" :isAdmin="true" />-->
   
    <br /><br />
    <div class="scrollable-container">
      <div class="container mt-3">
        <h2>{{ page_title }}</h2>
        <hr />
        <!-- capture the error here-->
        <p id="error" style="color: red;"></p>  
        <form @submit.prevent="createVenue" class="mx-auto" style="max-width: 400px;">
          <div class="form-group">
            <label for="venue_name">Venue name</label>
            <input v-model="venueData.name" type="text" class="form-control form-control-sm" id="venue_name" required maxlength="50">
            <div class="invalid-feedback">Venue name is required and should not exceed 50 characters.</div>
          </div>
          <div class="form-group">
            <label for="venue_description">Venue description</label>
            <textarea v-model="venueData.description" class="form-control form-control-sm" id="venue_description" rows="3" required maxlength="500"></textarea>
            <div class="invalid-feedback">Venue description is required and should not exceed 500 characters.</div>
          </div>
          <div class="form-group">
            <label for="venue_location">Venue location</label>
            <input v-model="venueData.location" type="text" class="form-control form-control-sm" id="venue_location" required maxlength="100">
            <div class="invalid-feedback">Venue location is required and should not exceed 100 characters.</div>
          </div>
          <div class="form-group">
            <label for="venue_capacity">Venue capacity</label>
            <input v-model="venueData.capacity" type="number" class="form-control form-control-sm" id="venue_capacity" required>
            <div class="invalid-feedback">Venue capacity is required and should be a valid number.</div>
          </div>
          <button type="submit" class="btn btn-primary btn-block">Create</button>
        </form>
      </div>
    </div>
    <br /><br /><br />
  </template>
  
  
  <script>
  //import navbar
  import api from "../api/api.js";

  export default {
    name: "CreateVenue",
    data() {
      return {
        page_title: "Create Venue",
        venueData: {
          name: "",
          description: "",
          location: "",
          capacity: null,
        },
      };
    },
    methods: {
      async createVenue() {

        //prepare the data to be sent to the server
        const data = {
          venue_name: this.venueData.name,
          venue_description: this.venueData.description,
          venue_location: this.venueData.location,
          venue_capacity: this.venueData.capacity,
        };

        //make an api call to create the venue
        const response = await api.post("create_venue", data);

        //check if the venue was created successfully
        if (response.status === 201) {
          //redirect to the admin dashboard
          this.$router.push("/admin_dashboard");
          
          //alert the user
            alert("Venue created successfully!");

          //force reload the page
          window.location.reload();

        
        } else {
          //display the error message
          document.getElementById("error").innerHTML = response.data.message;
        }

        
        console.log("Creating venue:", this.venueData);
      },
    },
  };
  </script>
  
  <style>
  h2 {
    text-align: center;
  }
  .scrollable-container {
  max-height: 400px; /* Set the desired height */
  overflow-y: auto; /* Add vertical scroll when content exceeds the height */
}
  </style>
  