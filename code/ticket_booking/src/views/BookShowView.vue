<template>
    <!-- add the nav bar -->
    <NavBarComponent :page_title="page_title" :isAdmin="false"/>
    <br /><br /><br />
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <h4>{{ show.show_name }}</h4>
          <p>{{ venue.venue_name }}</p>
        </div>
        <div class="col-md-6 text-right">
          <p>Date: {{ show.show_date }}</p>
          <p>Time: {{ show.show_time }}</p>
          <p>Tickets Available: {{ show.show_available_tickets }}</p>
          <p>Price: Rs {{ show.show_price }}</p>
        </div>
      </div>
      <hr />
      <form @submit.prevent="bookShow">
        <div class="form-group">
          <label for="tickets">Number of Tickets:</label>
          <input v-model="numTickets" type="number" class="form-control" id="tickets" name="tickets" required />
        </div>
        <button type="submit" class="btn btn-primary">Book Now</button>
      </form>
    </div>
  </template>
  
  <script>
    import api from "../api/api.js";
    import NavBarComponent from "../components/NavBarComponent.vue";
  
  export default {
    name: "BookShow",
    components: {
      NavBarComponent,
    },
    data() {
      return {
        page_title: "Book Show",
        show: {
          show_name: "Sample Show",
          show_date: "2023-07-31",
          show_time: "19:00",
          show_available_tickets: 50,
          show_price: 250,
          showId: null
        },
        venue: {
          venue_name: "Sample Venue",
        },
        numTickets: 0,
      };
    },
    mounted: async function () {

        //get the show id from the route
        this.showId = this.$route.params.show_id;
    
      const response = await api.get(`book_show/${this.showId}`);
      
        // Get the response data
        const responseData = response.data;

        if (responseData['success'] === true) {
          // Update the state
          this.show = responseData['data']['show'];
          this.venue = responseData['data']['venue'];
        } else {
          console.log('API request was successful, but response indicates failure.');
        }
    },
    methods: {
      bookShow: async function () {
        const bookingData = {
          show_id: this.show.id,
          tickets: this.numTickets,
        };

        //check if the the number of tickets that the user is trying to book if less that the available tickets
        if(this.numTickets > this.show.show_available_tickets){
          alert("Number of tickets requested is more than the available tickets");
          return;
        }


        const response = await api.post(`book_show/${this.showId}`, bookingData);

        const responseData = response.data;

        if (responseData['success'] === true) {
          alert('Show booked successfully!');

            this.$router.push('/user_dashboard');
        } else {
          alert('Show booking failed.');
        }

      },
    },
  };
  </script>
  
  <style scoped>
  h4{
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  h2 {
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  p {
    font-size: 18px;
    margin-bottom: 10px;
  }
  
  hr {
    margin-top: 30px;
    margin-bottom: 30px;
    border: none;
    border-top: 1px solid #ccc;
  }
  
  .form-group {
    /* align to center */
    margin: 0 auto;
    width: 50%;
  }
  
  .form-group label {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .form-control {
    height: 50px;
    font-size: 18px;
  }
  
  button.btn-primary {
    height: 50px;
    font-size: 18px;
    margin-top: 20px;
    /* center button */
    display: block;
    margin-left: auto;
    margin-right: auto;
  }
  </style>
  