<template>
  <div>
    <NavBarComponent :page_title="page_title" :isAdmin="true" />
    <div class="container mt-4">
      <h3>Statistics</h3>
      <br />
      <button @click="exportTable" class="btn btn-primary">Export Table</button>
      <table v-if="tableData.length > 0" class="table mt-4">
        <thead>
          <tr>
            <th v-for="header in tableHeaders" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in tableData" :key="row.id">
            <td v-for="header in tableHeaders" :key="header">{{ row[header] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="container mt-4">
      <h3>Graphs</h3>
      <img src="@/assets/summary_graph.png" alt="summary_graph" />
    </div>
  </div>
</template>

<script>
import NavBarComponent from "@/components/NavBarComponent.vue";
import api from "../api/api.js";

export default {
  name: "SummaryView",
  components: {
    NavBarComponent,
  },
  data() {
    return {
      page_title: "Statistics",
      tableHeaders: [], 
      tableData: [], 
    };
  },
  mounted() {
    api.get("summary")
  },

  //when this funciton is inserted in to the table , the data is created with a new instace which is then inserted into the tree
  methods: {
    // Function to load the CSV data
    exportTable() {
      const csvFilePath = require('@/assets/summary_graph.csv'); // Update with the correct path
      const link = document.createElement('a');
      link.href = csvFilePath;
      link.download = 'summary_graph.csv';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
  },

};
</script>

<style>
</style>
