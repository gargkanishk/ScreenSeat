<template>
    <PopUpModelComponent
        v-if="showPopUp"
        :page_title="popUpTitle"
        :modalId="'create-venue-modal'"
        :showId="clickedShowId"
      />
  <NavBarComponent :page_title="page_title" />
  <br /><br />
  <div class="container" v-if="venues.length">
    <div id="main-user-container">
      <div v-for="venue in venues" :key="venue.id" class="venue-container">
        <h3>{{ venue.venue_name }}</h3>
        <div v-if="venue.shows.length" class="show-container">
          <div v-for="show in venue.shows" :key="show.id" class="show-card">
            <h4>{{ show.show_name }}</h4>
            <p>{{ show.show_date }} | {{ show.show_time }}</p>
            <button class="book-now-btn" @click="handleClick('Book Show', null, show.id)">Book Now</button>
          </div>
        </div>
        <p v-else>No shows available.</p>
      </div>
    </div>
  </div>
  <div class="empty-message" v-else>
    <h5>No venues available, please check back later</h5>
    <hr />
  </div>
</template>

<script>
import NavBarComponent from "@/components/NavBarComponent.vue";
import api from '../api/api.js'
import PopUpModelComponent from "@/components/PopUpModelComponent.vue";

export default {
  name: "UserDashboard",
  components: {
    NavBarComponent,
    PopUpModelComponent
  },
  data() {
    return {
      page_title: "User Dashboard",
      venues: [],
        showPopUp: false,
        popUpTitle: "",
        clickedShowId: null,
    };
    },
    methods: {
      handleClick: function (title, venueId, showId) {
        this.popUpTitle = title;
        this.clickedShowId = showId;
        this.showPopUp = true;
      },
    },
    mounted: async function() {
  try {
    const response = await api.get('user_dashboard');

    const responseData = response.data;

    if (responseData['success'] === true) {
      this.venues = responseData['data'];
    } else {
      console.log('API request was successful, but response indicates failure.');
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
},

  };
  </script>
  
  <style>
  #main-user-container {
    margin-left: 30px;
    margin-right: 30px;
  }
  
  .empty-message {
    text-align: center;
    margin-top: 100px;
  }
  
  .venue-container {
    width: 100%;
    background-color: #f7f7f7;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
  }
  
  .show-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
  }
  
  .show-card {
    width: 250px;
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    margin-right: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  }
  
  .show-card h4 {
    margin-bottom: 10px;
  }
  
  .show-card p {
    margin-bottom: 5px;
  }
  
  .book-now-btn {
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 5px 15px;
    margin-top: 10px;
    cursor: pointer;
  }
  
  .book-now-btn:hover {
    background-color: #0062cc;
  }
  </style>
  