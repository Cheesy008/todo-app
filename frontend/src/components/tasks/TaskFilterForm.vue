<template>
  <app-card class="filter-card">
    <h2>Фильтрация</h2>
    <span class="filter-option">
      <label>Приоритет задачи</label>
        <select v-model="priority" class="filter-input">
          <option v-for="item in priorityTypes" :key="item.name" :value="item.type">
            {{ item.name }}
          </option>
        </select>
    </span>
    <span class="filter-option">
      <label>Статус задачи</label>
        <select v-model="status" class="filter-input">
          <option v-for="item in statusTypes" :key="item.name" :value="item.type">
            {{ item.name }}
          </option>
        </select>
    </span>
    <span class="filter-option">
      <label>Дэдлайн</label>
      <input type="date" class="filter-input" v-model="endDate"/>
    </span>
    <app-button type="info" @click="onSearch">Искать</app-button>
  </app-card>
</template>

<script>
import {mapMutations, mapActions} from 'vuex';

import {TaskPriority, TaskStatus} from "../../utils/enums";

export default {
  name: "TaskFilterForm",
  emits: ['update-tasks'],
  data() {
    return {
      status: null,
      priority: null,
      endDate: null,
      priorityTypes: [
        {type: null, name: 'Не указано'},
        {type: TaskPriority.LOW, name: 'Низкий'},
        {type: TaskPriority.MEDIUM, name: 'Средний'},
        {type: TaskPriority.HIGH, name: 'Высокий'},
      ],
      statusTypes: [
        {type: null, name: 'Не указано'},
        {type: TaskStatus.TODO, name: 'Надо сделать'},
        {type: TaskStatus.IN_PROGRESS, name: 'В процессе'},
        {type: TaskStatus.DONE, name: 'Сделано'},
      ],
    }
  },
  methods: {
    ...mapMutations('tasks', ['SAVE_FILTER_PARAMS']),
    ...mapActions('tasks', ['fetchTasks']),
    onSearch() {
      const filterParams = {
        'status': this.status,
        'priority': this.priority,
        'endDate': this.endDate
      }
      this.SAVE_FILTER_PARAMS(filterParams)
      this.$emit('update-tasks')
    },
  },
}
</script>

<style scoped lang="scss">
.filter-card {
  display: flex;
  flex-flow: column wrap;

  h2 {
    text-align: center;
  }

  .filter-option {
    margin: 15px;

    .filter-input {
      margin-left: 15px;
    }
  }
}

</style>