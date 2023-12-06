<template>
    <div>
      <NavBarComponent :page_title="page_title" />
      <br>
      <div class="row justify-content-center">
        <div class="col-md-6">
          <form @submit.prevent="search" class="input-group">
            <select v-model="searchSelector" class="form-control" required>
              <option value="venue">Venue</option>
              <option value="show">Show</option>
            </select>
            <input v-model="searchTerm" type="text" class="form-control" placeholder="Search for..." required>
            <div class="input-group-append">
              <button type="submit" class="btn btn-primary">Search</button>
            </div>
          </form>
        </div>
      </div>
  
      <div v-if="venues.length > 0" class="container mt-5 rounded bg-light">
        <h3 class="py-2">Venues:</h3>
        <div class="list-group">
          <div v-for="venue in venues" :key="venue.id" class="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <h5 class="mb-1">{{ venue.venue_name }}</h5>
              <p class="mb-1">{{ venue.venue_location }}</p>
            </div>
            <router-link :to="`/venue/${venue.id}`" class="btn btn-primary">View Venue</router-link>
          </div>
        </div>
      </div>
  
      <div v-if="shows.length > 0" class="container mt-5 rounded bg-light">
        <h3 class="py-2">Shows:</h3>
        <div class="list-group">
          <div v-for="show in shows" :key="show.id" class="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <h5 class="mb-1">{{ show.show_name }}</h5>
              <p class="mb-1">{{ show.venue_name }} - {{ show.show_date }}</p>
            </div>
            <router-link :to="`/book_show/${show.id}`" class="btn btn-primary">Book Show</router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import NavBarComponent from "@/components/NavBarComponent.vue";
  import api from "../api/api.js";
  
  export default {
    name: "SearchResults",
    components: {
      NavBarComponent
    },
    data() {
      return {
        page_title: "Search Results",
        searchSelector: "venue",
        searchTerm: "",
        venues: [],
        shows: []
      };
    },
    methods: {
      async search() {
        try {
          const response = await api.post("search/", {
            search_selector: this.searchSelector,
            search_term: this.searchTerm
          });

  
          const responseData = response.data;

          if (responseData.success === true) {
            if (this.searchSelector === "venue") {
                this.shows = [];
                this.venues = responseData.data;      
                console.log(this.venues);    
            } else {
            this.venues = [];
              this.shows = responseData.data;
            }

          } else {
            console.log("API request was successful, but response indicates failure.");
          }
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      }
    }
  };
  </script>
  
  