<template>
    <li>
      <input type="checkbox" v-model="task.completed">
      <span :class="{ 'completed': task.completed }">{{ task.text }}</span>
    </li>
  </template>
  
  <script>
  export default {
    props: ['task']
  };
  </script>
  
  <style>
  .completed {
    text-decoration: line-through;
  }
  </style>
  