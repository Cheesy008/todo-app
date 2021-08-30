<template>
  <teleport to="body">
    <div v-if="show" @click="tryClose" class="backdrop"></div>
    <transition name="dialog">
      <dialog open v-if="show">
        <header>
          <h2>Сообщение</h2>
        </header>
        <section>
          <ul>
            <li v-for="(message, index) in messages" :key="`${index}-${message}`">
              {{ message }}
            </li>
          </ul>
        </section>
        <menu>
          <app-button @click="tryClose">Закрыть</app-button>
        </menu>
      </dialog>
    </transition>
  </teleport>
</template>

<script>

export default {
  props: {
    messages: {
      type: Array,
      default: () => []
    },
  },
  emits: ['close'],
  computed: {
    show() {
      return this.messages.length;
    }
  },
  methods: {
    tryClose() {
      this.$emit('close');
    },
  },
};
</script>

<style scoped lang="scss">
.backdrop {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 10;
}

dialog {
  position: fixed;
  top: 20vh;
  left: 10%;
  width: 80%;
  z-index: 100;
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  padding: 0;
  margin: 0;
  overflow: hidden;
  background-color: white;
}

header {
  background-color: #f1f1f1;
  color: white;
  width: 100%;
  padding: 1rem;

  h2 {
    margin: 0;
    color: #000000;
  }
}

ul {
  list-style: none;
  li {
    font-size: 20px;
  }
}


section {
  padding: 1rem;
}

menu {
  padding: 1rem;
  display: flex;
  justify-content: flex-end;
  margin: 0;
}

.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.dialog-enter-active {
  transition: all 0.3s ease-out;
}

.dialog-leave-active {
  transition: all 0.3s ease-in;
}

.dialog-enter-to,
.dialog-leave-from {
  opacity: 1;
  transform: scale(1);
}

@media (min-width: 768px) {
  dialog {
    left: calc(50% - 20rem);
    width: 40rem;
  }
}

</style>