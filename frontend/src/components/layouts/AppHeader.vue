<template>
  <header>
    <app-dialog :messages="messages" @close="closeDialog"/>
    <h2>
      <router-link :to="{name: 'Home'}">Главная</router-link>
    </h2>
    <h3>Вы авторизованы под пользователем: {{ user.username }}</h3>
    <nav v-if="isAuthenticated">
      <ul class="buttons">
        <li>
          <AppButton type="info" @click="onSendStats">Отправить статистику</AppButton>
        </li>
        <li>
          <AppButton @click="onLogout">Выйти</AppButton>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'

import {messagesMixin} from "../../utils/mixins";

export default {
  mixins: [messagesMixin],
  computed: {
    ...mapGetters(['isAuthenticated', 'user'])
  },
  methods: {
    ...mapActions(['logout']),
    ...mapActions('tasks', ['sendStats']),
    async onLogout() {
      try {
        await this.logout();
        await this.$router.push({'name': 'Login'})
      } catch (e) {
        this.messages = e;
      }
    },
    async onSendStats() {
      try {
        await this.sendStats();
        this.messages.push('Статистика была успешно отправлена вам на почту')
      } catch (e) {
        this.messages = e;
      }
    },
  }
};
</script>

<style lang="scss" scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px;
  background-color: #3d008d;

  h2, h3 {
    color: #ffffff;
  }

  .buttons {
    list-style: none;

    li {
      display: inline-block;
      padding: 0 15px;
    }
  }

  a {
    font-weight: bold;
    color: #ffffff;
    text-decoration: none;
  }
}
</style>
