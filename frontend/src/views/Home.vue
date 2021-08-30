<template>
  <div>
    <app-dialog :messages="messages" @close="closeDialog"/>
    <section>
      <task-filter-form @update-tasks="loadTasks"/>
    </section>
    <section>
      <app-card class="home-card">
        <div class="controls">
          <app-button type="success" @click="createTaskForm">Создать задачу</app-button>
        </div>
        <div v-if="isLoading">
          <app-loader></app-loader>
        </div>
        <transition-group
            v-else
            tag="ul"
            name="task-list">
          <task-item
              v-for="(task, index) in tasks"
              :key="`${task.id}-${index}`"
              :task="task"
              :index="index"
              @delete-task="onDeleteTask"
              @update-tasks="loadTasks"
          ></task-item>
        </transition-group>
      </app-card>
    </section>
  </div>
</template>

<script>
import {mapActions} from 'vuex';

import TaskItem from "../components/tasks/TaskItem";
import {TaskPriority, TaskStatus} from "../utils/enums";
import TaskFilterForm from "../components/tasks/TaskFilterForm";
import {messagesMixin} from "../utils/mixins";

export default {
  name: 'Home',
  components: {TaskFilterForm, TaskItem},
  mixins: [messagesMixin],
  data() {
    return {
      isLoading: false,
      tasks: [],
      newTask: {
        id: null,
        description: '',
        priority: TaskPriority.LOW,
        status: TaskStatus.TODO,
        end_date: null,
      }
    }
  },
  methods: {
    ...mapActions('tasks', ['fetchTasks', 'deleteTask']),
    async loadTasks() {
      this.isLoading = true;
      try {
        await this.fetchTasks();
        this.tasks = JSON.parse(JSON.stringify(this.$store.getters['tasks/getTasks']))
      } catch (e) {
        this.messages = e;
      }
      this.isLoading = false;
    },
    createTaskForm() {
      this.tasks.unshift(this.newTask);
    },
    async onDeleteTask(taskId, taskIndex) {
      if (taskId === null) {
        this.tasks.splice(taskIndex, 1)
      } else {
        try {
          await this.deleteTask(taskId)
          this.tasks.splice(taskIndex, 1)
        } catch (e) {
          this.messages = e;
        }
      }
    }
  },
  created() {
    this.loadTasks()
  }
}
</script>

<style lang="scss">
ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.controls {
  display: flex;
  justify-content: space-between;
}

.home-card {
  min-height: 500px;
}

.task-list-enter-from {
  opacity: 0;
  transform: scale(0.6);
}

.task-list-enter-to {
  opacity: 1;
  transform: scale(1);
}

.task-list-enter-active {
  transition: all 0.4s ease;
}

.task-list-leave-from {
  opacity: 1;
  transform: scale(1);
}

.task-list-leave-to {
  opacity: 0;
  transform: scale(0.6);
}

.task-list-leave-active {
  transition: all 0.4s ease;
}


</style>
