<template>
    <div>
      <PopUpModelComponent
        v-if="showPopUp"
        :page_title="popUpTitle"
        :modalId="'create-venue-modal'"
        :venueId="clickedVenueId"
        :showId="clickedShowId"
      />
  
      <NavBarComponent :page_title="page_title" :isAdmin="true" />
  
      <div>
        <br /><br />
  
        <div class="container empty-message" v-if="venues.length === 0">
          <h5>No venues available, please create a new venue</h5>
          <hr />
        </div>
  
        <div id="venues-container">
          <div v-for="venue in venues" :key="venue.id" class="card mr-2" style="border-radius: 10px;">
            <div class="card-header">
              <h5>{{ venue.venue_name }}</h5>
            </div>
            <div class="card-body">
              <p v-if="!venue.shows.length" id="empty-showlist">No shows available<br />Create a new show please</p>
              <div v-for="show in venue.shows" :key="show.id">
                <p>{{ show.show_name }} - {{ show.show_date }}</p>
                <div class="btn-group">
                  <button
                    type="button"
                    class="btn btn-sm btn-primary dropdown-toggle"
                    :class="{ show: isDropdownOpen(venue.id, show.id) }"
                    @click="toggleDropdown(venue.id, show.id)"
                  >
                    Actions
                  </button>
                  <div class="dropdown-menu dropdown-menu-right" :class="{ show: isDropdownOpen(venue.id, show.id) }">
                    <button @click="handleClick('Edit Show', venue.id, show.id)" class="dropdown-item">Edit</button>
                    <a class="dropdown-item" @click="confirmDelete(show.id)">Delete</a>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer d-flex justify-content-between">
              <button @click="handleClick('Edit Venue', venue.id)" class="btn btn-primary">Edit</button>
              <a @click="confirmDeleteVenue(venue.id)" class="btn btn-danger">Delete</a>
              <button @click="handleClick('Create Show', venue.id, null)" class="btn btn-success">
                <i class="fas fa-plus"></i>
              </button>
            </div>
          </div>
        </div>
  
        <!-- Add the data-toggle and data-target attributes to trigger the modal -->
        <button
          @click="handleClick('Create Venue', null)"
          class="btn btn-primary fixed-button d-flex justify-content-center align-items-center"
          data-toggle="modal"
          data-target="#create-venue-modal"
          title="Create new Venue"
        >
          <i class="fas fa-plus"></i>
        </button>
      </div>
    </div>
  </template>
  
  
  
  
  <script>
  import api from "../api/api.js";
  import NavBarComponent from "@/components/NavBarComponent.vue";
  import PopUpModelComponent from "@/components/PopUpModelComponent.vue";
  
  export default {
    name: "AdminDashboard",
    components: {
      NavBarComponent,
        PopUpModelComponent,
    },
    data() {
      return {
        venues: [], 
        page_title: "Admin Dashboard",
        dropdownStates: {}, 
        showPopUp: false, 
        popUpTitle: "Create Venue", 
        clickedVenueId: null,
        clickedShowId: null,
      };
    },
    methods: {
      async confirmDelete(showId) {
        if (confirm('Are you sure you want to delete this show? All its bookings will also be deleted')) {
            // Call the API to delete the show
            const response = await api.get(`delete_show/${showId}`);
            // Get the response data
            const responseData = response.data;

            if(responseData['success']==true){
                alert("Show has been deleted successfully");
                location.reload();
            } else{
                alert("Show could not be deleted, something went wrong")

            }
        }
      },
      handleClick(title, venueId, showId) {
        this.clickedVenueId = venueId;
        this.clickedShowId = showId;
        this.popUpTitle = title;
        this.showPopUp = true;
      },
      async confirmDeleteVenue(venueId) {
        if (confirm('Are you sure you want to delete this venue? All its shows and bookings would also be deleted!')) {
          const response = await api.get(`delete_venue/${venueId}`);
          const responseData = response.data;
          if (responseData['success'] === true) {
            alert("Venue has been deleted successfully");
            location.reload();
          } else {
            alert("Venue could not be deleted, something went wrong");
          }
          console.log('Deleting venue with ID:', venueId);
        }
      },
      toggleDropdown(venueId, showId) {
        const key = `${venueId}_${showId}`;
        this.dropdownStates[key] = !this.dropdownStates[key];
      },
      isDropdownOpen(venueId, showId) {
        const key = `${venueId}_${showId}`;
        return this.dropdownStates[key];
      },
    },
    mounted: async function () {
      const response = await api.get('admin_dashboard');
      const responseData = response.data;
      if (responseData['success'] === true) {
        this.venues = responseData['data'];
      } else {
        console.log('API request was successful, but response indicates failure.');
      }
    },
  };
  </script>
  
  
  <style>
  #empty-showlist {
    text-align: center;
    margin-top: 20px;
  }
  .empty-message {
    text-align: center;
    margin-top: 100px;
  }
  
  .fixed-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 99;
  }
  .fixed-button.btn-primary {
    border-radius: 50%;
    width: 60px;
    height: 60px;
    line-height: 50px;
    font-size: 24px;
    text-align: center;
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
  }
  .fixed-button.btn-primary i {
    line-height: 60px;
  }
  #venues-container {
    display: flex;
    flex-wrap: wrap;
  }
  
  .card {
    margin: 10px;
    width: 250px;
  }
  </style>
  