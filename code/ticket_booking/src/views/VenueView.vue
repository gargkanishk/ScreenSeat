<template>
    <div>
      <!-- include the navbar component here -->
      <NavBarComponent :page_title="pageTitle" />
      <br>
      <div class="container venue-container">
        <div class="row">
          <div class="col-md-6">
            <h2>{{ venue.venue_name }}</h2>
            <p>{{ venue.venue_description }}</p>
            <p><strong>Location:</strong> {{ venue.venue_location }}</p>
            <p><strong>Capacity:</strong> {{ venue.venue_capacity }}</p>
          </div>
          <div class="col-md-6">
            <img src="../assets/venue-placeholder.jpg" alt="Venue Image" class="img-fluid">
          </div>
        </div>
        <hr>
        <h3>Shows:</h3>
        <div v-if="shows!=[]" class="row">
          <div v-for="show in venue.shows" :key="show.id" class="col-md-4">
            <div class="card show-card">
              <img src="../assets/show-placeholder.jpg" class="card-img-top" alt="Show Image">
              <div class="card-body">
                <h5 class="card-title">{{ show.show_name }}</h5>
                <p class="card-text">{{ show.show_date }}</p>
                <p class="card-text"><strong>Price:</strong> {{ show.show_price }}</p>
                <p class="card-text"><strong>Tags:</strong> {{ show.show_tags }}</p>
                <button v-if="show.show_available_tickets > 0" @click="bookShow(show.id)" class="btn btn-primary">Book Now</button>
                <button v-else class="btn btn-danger" disabled>Tickets Unavailable</button>
              </div>
            </div>
          </div>
        </div>
        <p v-else>No shows found for this venue.</p>
      </div>
    </div>
  </template>
  
  <script>
  import NavBarComponent from "@/components/NavBarComponent.vue";
    import api from "../api/api.js";
  
  export default {
    name: "VenueDetails",
    components: {
      NavBarComponent
    },

    data() {
      return {
        venueId: null, 
        pageTitle: "Venue Details", 
        venue: {}, 
        shows: [] 
      };
    },
    mounted : async function (){
        this.venueId = this.$route.params.venue_id;
      const response = await api.get(`venue_details/${this.venueId}`);
      const responseData = response.data;

      if (responseData["success"] === true) {
        this.venue = responseData["data"]['venue'];
        this.pageTitle = this.venue.venue_name;

        this.shows = this.venue.shows; 
      } else {
        console.log("API request was successful, but response indicates failure.");
      }
    },
    methods: {
        //function to route to book show view
        bookShow(showId) {
          this.$router.push(`/book_show/${showId}`);
        }
    },
  };
  </script>
  
  <style>
    .venue-container {
      margin-top: 50px;
      margin-bottom: 50px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      padding: 30px;
    }
  
    .show-card {
      margin-bottom: 30px;
    }
  
    .show-card img {
      height: 200px;
      object-fit: cover;
    }
  </style>
  