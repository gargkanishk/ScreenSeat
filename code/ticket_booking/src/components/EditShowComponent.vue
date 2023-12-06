<template>
    <!-- Add the navbar and pass the page title and isAdmin -->

    <div class="container mt-3 scrollable-container">
      <h2>{{ page_title }}</h2>
      <hr>
      <form @submit.prevent="updateShow" class="mx-auto" style="max-width: 400px;">
        <div class="form-group">
          <label for="show_name">Show name</label>
          <input v-model="showData.show_name" type="text" class="form-control form-control-sm" id="show_name" required>
        </div>
        <div class="form-group">
          <label for="show_date">Show date</label>
          <input v-model="showData.show_date" type="date" class="form-control form-control-sm" id="show_date" required>
        </div>
        <div class="form-group">
          <label for="show_time">Show time</label>
          <input v-model="showData.show_time" type="time" class="form-control form-control-sm" id="show_time" required>
        </div>
        <div class="form-group">
          <label for="show_price">Show price</label>
          <input v-model="showData.show_price" type="number" class="form-control form-control-sm" id="show_price" required>
        </div>
        <div class="form-group">
          <label for="show_tags">Show tags</label>
          <input v-model="showData.show_tags" type="text" class="form-control form-control-sm" id="show_tags" required>
        </div>
  
        <button type="submit" class="btn btn-primary btn-block">Update</button>
      </form>
    </div>
  </template>
  
  <script>
  // Import navbar component and other necessary dependencies
  import api from "../api/api.js";
  
  export default {
    name: "EditShow",
    props: {
      showId: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        page_title: "Edit Show",
        showData: {
          show_name: "", // Initialize with empty values
          show_rating: "",
          show_date: "",
          show_time: "",
          show_price: "",
          show_tags: "",
        },
      };
    },
    mounted: async function () {
      // Make an API call to get the show details
      const response = await api.get(`show_details/${this.showId}`);
      // Get the response data
      this.showData = response.data.data.show;
    },
    methods: {
      async updateShow() {
        // Prepare the data to be sent to the API
        const data = {
          show_name: this.showData.show_name,
          show_date: this.showData.show_date,
          show_time: this.showData.show_time,
          show_price: this.showData.show_price,
          show_tags: this.showData.show_tags,
        };
  
        const response = await api.post(`edit_show/${this.showId}`, data);
  
        // Check if the response is successful
        if (response.status === 201) {
          // Alert the user
          alert("Show updated successfully!");
          
          //reload the page
          window.location.reload();
        } else {
          // Display the error message
          console.error(response.data.message);
        }
      },
    },
  };
  </script>
  
  <style>
  /* Your component's styles go here */
  h2 {
    text-align: center;
  }
  .scrollable-container {
  max-height: 400px; /* Set the desired height */
  overflow-y: auto; /* Add vertical scroll when content exceeds the height */
}
  </style>
  