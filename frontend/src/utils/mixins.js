export const messagesMixin = {
    data() {
        return {
            messages: []
        }
    },
    methods: {
        closeDialog() {
            this.messages = []
        }
    }
}