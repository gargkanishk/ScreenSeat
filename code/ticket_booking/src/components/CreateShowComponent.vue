<template>
    <!-- Add the navbar and pass the page title and isAdmin -->
  
    <div class="container mt-3 scrollable-container">
      <h2>{{ page_title }}</h2>
      <hr>
        <!-- capture the error here-->
        <p id="error" style="color: red;"></p>
      <form @submit.prevent="createShow" class="mx-auto" style="max-width: 400px;">
        <div class="form-group">
          <label for="show_name">Show name</label>
          <input v-model="showData.name" type="text" class="form-control form-control-sm" id="show_name" required>
        </div>
        <div class="form-group">
          <label for="show_date">Show date</label>
          <input v-model="showData.date" type="date" class="form-control form-control-sm" id="show_date" required>
        </div>
        <div class="form-group">
          <label for="show_time">Show time</label>
          <input v-model="showData.time" type="time" class="form-control form-control-sm" id="show_time" required>
        </div>
        <div class="form-group">
          <label for="show_price">Show price</label>
          <input v-model="showData.price" type="number" class="form-control form-control-sm" id="show_price" required>
        </div>
        <div class="form-group">
          <label for="show_tags">Show tags</label>
          <input v-model="showData.tags" type="text" class="form-control form-control-sm" id="show_tags" required>
        </div>
        <div class="form-group">
          <label for="show_capacity">Show capacity</label>
          <input v-model="showData.capacity" type="number" class="form-control form-control-sm" id="show_capacity" required>
        </div>
        <div class="form-group">
          <label for="venue_name">Venue name</label>
          <input v-model="venueData.venue_name" type="text" class="form-control form-control-sm" id="venue_name" :readonly="true">
        </div>
  
        <button type="submit" class="btn btn-primary btn-block">Create</button>
      </form>
    </div>
    <br /><br /><br />
  </template>
  
  <script>
  // Import navbar
 import api from "../api/api.js";

  
  export default {
    name: "CreateShow",
    props: {
      venueId: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        page_title: "Create Show",
        showData: {
          name: "",
          date: "",
          time: "",
          price: "",
          tags: "",
          capacity: null,
        },
        venueData: {
          venue_name: "Venue Name", // Replace with actual data from API or Vuex store
        },
      };
    },
    mounted: async function () {
      // Make an API call to get the venue details
      const response = await api.get(`venue_details/${this.venueId}`);
      // Get the response data
      this.venueData = response.data.data.venue;
    },
    methods: {
      async createShow() {

        //prepare the data to be sent to the API
        const data = {
          show_name: this.showData.name,
          show_date: this.showData.date,
          show_time: this.showData.time,
          show_price: this.showData.price,
          show_tags: this.showData.tags,
          show_capacity: this.showData.capacity,
          venue_name: this.venueData.venue_name,
        };

        const response = await api.post(`create_show/${this.venueId}`, data);

        //check if the response is successful
        if (response.status === 201) {

        //alert the user
            alert("Show created successfully!");
          
            //reload the page
            window.location.reload();
        } else {
          //display the error message
          document.getElementById("error").innerHTML = response.data.message;
        }
        console.log("Creating show:", this.showData);
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
  