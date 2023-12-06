<template>
  <div>
    <NavBarComponent :page_title="page_title" />
    <div class="container">
      <h1 class="mb-4">My Bookings</h1>
      <div v-if="bookings && Object.keys(bookings).length > 0">
        <div class="row">
          <div
            v-for="(booking, key) in bookings"
            :key="key"
            class="col-md-4 mb-4"
          >
            <div class="card" style="border-radius: 10px;">
              <div class="card-body">
                <h5 class="card-title">{{ booking.show_name }}</h5>
                <div class="row">
                  <div class="col-md-6">
                    <p class="card-text"><strong>Venue:</strong> {{ booking.venue_name }}</p>
                    <p class="card-text"><strong>Date:</strong> {{ booking.show_date }}</p>
                    <p class="card-text"><strong>Time:</strong> {{ booking.show_time }}</p>
                  </div>
                  <div class="col-md-6">
                    <p class="card-text"><strong>Tickets:</strong> {{ booking.tickets }}</p>
                    <p class="card-text"><strong>Total Price:</strong> {{ booking.total_price }}</p>
                    <template v-if="booking.show_rating === null">
                      <!--- show stars to rate the show-->
                      <div class="rating">
                        <span v-for="n in 5" :key="n" class="star" @click="rateShow(booking.id, n)">
                          <i v-if="n <= (tempRating || booking.show_rating)" class="fas fa-star"></i>
                          <i v-else class="far fa-star"></i>
                        </span>
                      </div>
                    </template>
                    <template v-else>
                      <p class="card-text"><strong>Rating:</strong> {{ booking.show_rating }}/5</p>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>You haven't booked any shows yet.</p>
      </div>
    </div>
  </div>
</template>


  
  <script>
  import NavBarComponent from "@/components/NavBarComponent.vue";
    import api from "../api/api.js";
  
  export default {
    name: "MyBookings",
    components: {
      NavBarComponent
    },
    data() {
      return {
        page_title: "My Bookings",
        bookings: [], // Initialize the bookings array
        tempRating: null
      };
    },
    mounted: async function()  {
        try {

          const user_id = localStorage.getItem('user_id');
      
          const response = await api.get(`my_bookings/${user_id}`);
  
          if (response && response.data.success) {
            this.bookings = response.data.data;
          } else {
            console.log("API request was successful, but response indicates failure.");
          }
        } catch (error) {
          console.error("Error fetching data:", error);
        }

    },
    methods: {
      async rateShow(bookingId, rating) {
        try {
          const response = await api.post(`rate_show/${bookingId}`, {
            show_rating: rating
          });
  
          if (response && response.data.success) {
            //notify the user
            alert(response.data.message)
            this.tempRating = rating;
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
  
  <style>
  .card {
    border: none;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    padding: 20px;
    border-radius: 5px;
  }
  
  .card-title {
    margin-bottom: 20px;
  }
  
  .card-text {
    margin-bottom: 10px;
  }
  
  .btn-primary {
    background-color: #2d3e50;
    border: none;
  }
  
  .btn-primary:hover {
    background-color: #34495e;
  }
  </style>
  