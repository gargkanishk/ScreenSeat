<template>
    <ul>
      <TodoItem v-for="task in tasks" :key="task.id" :task="task" />
    </ul>
  </template>
  
  <script>
  import TodoItem from './TodoItem.vue';
  
  export default {
    components: {
      TodoItem
    },
    props: ['tasks']
  };
  </script>
  