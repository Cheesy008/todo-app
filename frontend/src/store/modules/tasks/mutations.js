export default {
    SET_TASKS(state, payload) {
        state.tasks = payload;
    },
    SAVE_FILTER_PARAMS(state, payload) {
        state.filterParams = payload;
    }
}