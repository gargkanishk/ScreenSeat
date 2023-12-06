<template>
  
    <br /><br />
    <div>
      <div class="container mt-3 scrollable-container">
        <h2>{{ page_title }}</h2>
        <hr />
        <!-- capture the error here-->
        <p id="error" style="color: red;"></p>
  
        <form @submit.prevent="updateVenue" class="mx-auto" style="max-width: 400px;">
          <div class="form-group">
            <label for="venue_name">Venue name</label>
            <input v-model="venueInfo.name" type="text" class="form-control form-control-sm" id="venue_name" required maxlength="50">
            <div class="invalid-feedback">Venue name is required and should not exceed 50 characters.</div>
          </div>
          <div class="form-group">
            <label for="venue_description">Venue description</label>
            <textarea v-model="venueInfo.description" class="form-control form-control-sm" id="venue_description" rows="3" required maxlength="200"></textarea>
            <div class="invalid-feedback">Venue description is required and should not exceed 200 characters.</div>
          </div>
          <div class="form-group">
            <label for="venue_location">Venue location</label>
            <input v-model="venueInfo.location" type="text" class="form-control form-control-sm" id="venue_location" required maxlength="100">
            <div class="invalid-feedback">Venue location is required and should not exceed 100 characters.</div>
          </div>
          <div class="form-group">
            <label for="venue_capacity">Venue capacity</label>
            <input v-model="venueInfo.capacity" type="number" class="form-control form-control-sm" id="venue_capacity" required>
            <div class="invalid-feedback">Venue capacity is required and should be a valid number.</div>
          </div>
          <button type="submit" class="btn btn-primary btn-block">Update</button>
        </form>
      </div>
    </div>
    <br /><br /><br />
  </template>
  
  <script>
  // Import navbar
    import api from "../api/api.js";
  
  export default {
    name: "EditVenue",
    props: {
      venueId: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        page_title: "Edit Venue",
        venueInfo: {
          name: "Venue Name", // Replace with actual data from API or Vuex store
          description: "Venue Description", // Replace with actual data from API or Vuex store
          location: "Venue Location", // Replace with actual data from API or Vuex store
          capacity: 100, // Replace with actual data from API or Vuex store
        },
        temp: {},
      };
    },
    mounted: async function () {
        // Make an API call to get the venue details
        const response = await api.get(`venue_details/${this.venueId}`);
        // Get the response data
        const venueData = response.data.data.venue;

        // Update the venueInfo object with the response data
        this.venueInfo.name = venueData.venue_name;
        this.venueInfo.description = venueData.venue_description;
        this.venueInfo.location = venueData.venue_location;
        this.venueInfo.capacity = venueData.venue_capacity;

    },
    methods: {
      async updateVenue() {

        //prepare the venue info object
        this.temp = {
          venue_name: this.venueInfo.name,
            venue_description: this.venueInfo.description,
            venue_location: this.venueInfo.location,
            venue_capacity: this.venueInfo.capacity,
        };
        
        // Make an API call to update the venue details
        const response = await api.post(`update_venue/${this.venueId}`, this.temp);
        // Get the response data
        const responseData = response.data;
        // Check if the response data has the success message
        if (responseData["success"] === true) {
          

          alert("Venue updated successfully");

          //reload the page
          window.location.reload();

        } else {
          // Display the error message
          document.getElementById("error").innerHTML = responseData.error;
        }
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
  