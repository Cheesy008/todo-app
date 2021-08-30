<template>
  <li>
    <app-dialog :messages="messages" @close="closeDialog"/>
    <form @submit.prevent>
      <div class="form-control">
        <label>Текст задачи</label>
        <input type="text" v-model.trim="taskCopy.description"/>
        <span v-if="v$.taskCopy.description.$error">Текст обязателен к заполнению.</span>
      </div>
      <div class="form-control">
        <label>Приоритет задачи</label>
        <select v-model="taskCopy.priority">
          <option v-for="item in priorityTypes" :key="item.name" :value="item.type">
            {{ item.name }}
          </option>
        </select>
      </div>
      <div class="form-control">
        <label>Статус задачи</label>
        <select v-model="taskCopy.status">
          <option v-for="item in statusTypes" :key="item.name" :value="item.type">
            {{ item.name }}
          </option>
        </select>
        <span v-if="v$.taskCopy.status.$error">Статус задачи обязателен к заполнению.</span>
      </div>
      <div class="form-control">
        <label>Дэдлайн</label>
        <input type="date" v-model="taskCopy.end_date"/>
      </div>
      <div class="buttons">
        <app-button type="success" @click.prevent="submitForm">{{ submitButtonName }}</app-button>
        <app-button type="danger" @click="deleteTask">Удалить</app-button>
      </div>
    </form>
  </li>
</template>

<script>
import useValidate from '@vuelidate/core'
import {required} from '@vuelidate/validators'
import {mapActions} from "vuex";

import {TaskPriority, TaskStatus} from "../../utils/enums";
import {messagesMixin} from "../../utils/mixins";

export default {
  name: "TaskItem",
  props: {
    index: {
      type: Number,
      required: true
    },
    task: {
      type: Object,
      required: true
    }
  },
  emits: ['delete-task', 'update-tasks'],
  mixins: [messagesMixin],
  data() {
    return {
      v$: useValidate(),
      taskCopy: {...this.task},
      priorityTypes: [
        {type: null, name: 'Не указано'},
        {type: TaskPriority.LOW, name: 'Низкий'},
        {type: TaskPriority.MEDIUM, name: 'Средний'},
        {type: TaskPriority.HIGH, name: 'Высокий'},
      ],
      statusTypes: [
        {type: TaskStatus.TODO, name: 'Надо сделать'},
        {type: TaskStatus.IN_PROGRESS, name: 'В процессе'},
        {type: TaskStatus.DONE, name: 'Сделано'},
      ],
    }
  },
  validations() {
    return {
      taskCopy: {
        description: {
          required,
        },
        status: {
          required,
        },
      }
    }
  },
  computed: {
    isCreated() {
      return !!this.task.id
    },
    submitButtonName() {
      return this.isCreated ? 'Редактировать' : 'Создать';
    }
  },
  methods: {
    ...mapActions('tasks', ['createTask', 'updateTask', 'fetchTasks']),
    async submitForm() {
      this.v$.$validate();
      if (this.v$.$error) {
        return
      }
      const payload = {
        id: this.taskCopy.id,
        description: this.taskCopy.description,
        status: this.taskCopy.status,
        priority: this.taskCopy.priority,
        end_date: this.taskCopy.end_date,
      }
      
      try {
        if (!this.isCreated) {
          await this.createTask(payload);
        } else {
          await this.updateTask(payload);
        }
        this.$emit('update-tasks');
      } catch (e) {
        this.messages = e
      }
    },
    deleteTask() {
      this.$emit('delete-task', this.taskCopy.id, this.index)
    }
  },
}
</script>

<style scoped lang="scss">
@import "src/assets/scss/app-form";

li {
  margin: 1rem 0;
  border: 1px solid #424242;
  border-radius: 12px;
  padding: 1rem;
}

</style>