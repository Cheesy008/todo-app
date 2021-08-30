<template>
  <div>
    <app-dialog @close="closeDialog" :messages="messages"/>
    <app-card>
      <div v-if="isLoading">
        <app-loader></app-loader>
      </div>
      <form @submit.prevent="submitForm">
        <div class="form-control">
          <label for="username">E-mail</label>
          <input type="text" id="email" v-model.trim="form.email"/>
          <span v-if="v$.form.email.$error">E-mail является невалидным.</span>
        </div>
        <div class="form-control">
          <label for="username">Никнейм</label>
          <input type="text" id="username" v-model.trim="form.username"/>
          <span v-if="v$.form.username.$error">Длина никнейма должна составлять не менее четырёх символов.</span>
        </div>
        <div class="form-control">
          <label for="password">Пароль</label>
          <input type="password" id="password" v-model.trim="form.password"/>
          <span v-if="v$.form.password.$error">Длина пароля должна составлять не менее шести символов.</span>
        </div>
        <div class="form-control">
          <label for="password-confirmation">Повторить пароль</label>
          <input type="password" id="password-confirmation" v-model.trim="form.passwordConfirmation"/>
          <span v-if="v$.form.passwordConfirmation.$error">Пароли не совпадают.</span>
        </div>
        <div class="buttons">
          <app-button :disabled="isSubmitButtonDisabled" type="info">Зарегистрироваться</app-button>
          <app-button @click="this.$router.push({'name': 'Login'})">Войти
          </app-button>
        </div>
      </form>
    </app-card>
  </div>
</template>


<script>
import useValidate from '@vuelidate/core'
import {required, minLength, email, sameAs} from '@vuelidate/validators'
import {mapActions} from 'vuex'

import {AuthFormTypes} from "../utils/enums";
import {messagesMixin} from "../utils/mixins";

export default {
  mixins: [messagesMixin],
  data() {
    return {
      v$: useValidate(),
      form: {
        email: '',
        username: '',
        password: '',
        passwordConfirmation: '',
      },
      isLoading: false,
    }
  },
  validations() {
    return {
      form: {
        email: {
          required,
          email
        },
        username: {
          required,
          minLength: minLength(4)
        },
        password: {
          required,
          minLength: minLength(6)
        },
        passwordConfirmation: {
          sameAsPassword: sameAs(this.form.password)
        }
      }
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
        formType: AuthFormTypes.REGISTER,
        email: this.form.email,
        username: this.form.username,
        password: this.form.password,
        password_confirmation: this.form.passwordConfirmation,
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