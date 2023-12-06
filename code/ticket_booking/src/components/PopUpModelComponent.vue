<template>
    <div :class="['modal', { show: showModal }]">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ page_title }}</h5>
            <button type="button" class="close" @click="closeModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <!-- Use v-if to conditionally render the component based on page title --> 
            <template v-if="page_title === 'Create Venue'">
              <CreateVenue/>
            </template>
            <template v-else-if="page_title === 'Create Show'">
              <CreateShow :venueId="venueId" />
            </template>
            <template v-else-if="page_title === 'Edit Venue'">
              <EditVenue :venueId="venueId" />
            </template>
            <template v-else-if="page_title === 'Edit Show'">
              <EditShow :showId="showId" />
            </template>
            <!-- template for book show-->
            <template v-else-if="page_title === 'Book Show'">
              <BookShow :showId="showId" />
            </template>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  // Import the components that will be displayed in the modal
  import CreateVenue from "./CreateVenueComponent.vue";
    import CreateShow from "./CreateShowComponent.vue";
    import EditVenue from "./EditVenueComponent.vue";
    import EditShow from "./EditShowComponent.vue";
    import BookShow from "./BookShowComponent.vue";

  
  export default {
    name: "PopUpModelComponent",
    components: {
      CreateVenue,
        CreateShow,
        EditVenue,
        EditShow,
        BookShow,
    },
    props: {
      modalId: {
        type: String,
        required: true,
      },
      page_title: {
        type: String,
        required: true,
      },
      venueId: {
        type: Number,
        required: false,
      },
        showId: {
            type: Number,
            required: false,
        },
    },
    data() {
      return {
        showModal: true,
      };
    },
    methods: {
      openModal() {
        this.showModal = true;
        // Optionally, you can add additional logic here, such as preventing scrolling when the modal is open.
      },
      closeModal() {
        
        //for reloading the page
        window.location.reload();
        
      },
    },
  };
  </script>
  
  <style>
  /* Add any custom styles for the modal here */
  .modal {
    display: none; /* Hide the modal by default */
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black background */
  }
  
  .modal.show {
    display: block; /* Show the modal when 'showModal' is true */
  }
  
  .modal-dialog {
    margin: 10% auto; /* Center the modal vertically */
    width: 80%;
    max-width: 400px; /* Set maximum width for the modal */
    background-color: #fff; /* White background for the modal */
    border: 1px solid #888;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .modal-content {
    padding: 16px;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 1px solid #eee;
  }
  
  .modal-title {
    font-size: 18px;
    font-weight: bold;
  }
  
  .modal-body {
    padding: 16px 0;
  }
  
  .modal-footer {
    display: flex;
    justify-content: flex-end;
    padding-top: 8px;
    border-top: 1px solid #eee;
  }
  </style>
  