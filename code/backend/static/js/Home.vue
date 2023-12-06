<template>
    <div>
      <input v-model="newTask" @keyup.enter="addTask" placeholder="Enter a new task...">
      <TodoList :tasks="tasks" />
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        newTask: '',
        tasks: []
      };
    },
    methods: {
      addTask() {
        if (this.newTask.trim() !== '') {
          this.tasks.push({
            id: Date.now(),
            text: this.newTask,
            completed: false
          });
          this.newTask = '';
        }
      }
    }
  };
  </script>
  