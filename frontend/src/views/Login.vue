<template>
  <div>
    <app-dialog @close="closeDialog" :messages="messages"/>
    <app-card>
      <div v-if="isLoading">
        <app-loader></app-loader>
      </div>
      <form @submit.prevent="submitForm" v-else>
        <h1>Войти</h1>
        <div class="form-control">
          <label for="username">Никнейм</label>
          <input type="text" id="username" v-model.trim="form.username"/>
          <span v-if="v$.form.username.$error">Длина никнейма должна составлять не менее трёх символов.</span>
        </div>
        <div class="form-control">
          <label for="password">Пароль</label>
          <input type="password" id="password" v-model.trim="form.password"/>
          <span v-if="v$.form.password.$error">Длина пароля должна составлять не менее трёх символов.</span>
        </div>
        <div class="buttons">
          <app-button :disabled="isSubmitButtonDisabled">Войти</app-button>
          <app-button
              type="info"
              @click="this.$router.push({'name': 'Register'})">Зарегистрироваться
          </app-button>
        </div>
      </form>
    </app-card>
  </div>
</template>


<script>
import useValidate from '@vuelidate/core'
import {required, minLength} from '@vuelidate/validators'
import {mapActions} from 'vuex'

import {AuthFormTypes} from "../utils/enums";
import {messagesMixin} from "../utils/mixins";

export default {
  mixins: [messagesMixin],
  data() {
    return {
      v$: useValidate(),
      form: {
        username: '',
        password: '',
      },
      isLoading: false,
    }
  },
  validations: {
    form: {
      username: {
        required,
        minLength: minLength(3)
      },
      password: {
        required,
        minLength: minLength(3)
      },
    }
  },
  computed: {
    isSubmitButtonDisabled() {
      return this.v$.$error;
    }
  },
  methods: {
    ...mapActions(['auth']),
    async submitForm() {
      this.v$.$validate();
      if (this.v$.$error) {
        return
      }
      this.isLoading = true;

      const payload = {
        formType: AuthFormTypes.LOGIN,
        username: this.form.username,
        password: this.form.password,
      };

      try {
        await this.auth(payload);
        await this.$router.push({'name': 'Home'})
      } catch (e) {
        this.messages = e;
      }

      this.isLoading = false;
    },
  }
}
</script>

<style lang="scss">
@import "src/assets/scss/app-form";

</style>