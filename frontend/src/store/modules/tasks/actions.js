import errorParser from "../../../utils/errorParser";

export default {
    async fetchTasks({commit, state}) {
        let {status, priority, endDate} = state.filterParams;
        status = status !== null ? status : '';
        priority = priority !== null ? priority : '';
        endDate = endDate ? endDate : '';

        try {
            const resp = await this.$axios.get(`task/?priority=${priority}&status=${status}&end_date=${endDate}`);
            commit('SET_TASKS', resp.data)
        } catch (e) {
            return errorParser(e)
        }
    },
    async createTask(_, payload) {
        try {
            await this.$axios.post('task/', payload);
        } catch (e) {
            return errorParser(e)
        }
    },
    async updateTask(_, payload) {
        try {
            await this.$axios.patch(`task/${payload.id}/`, payload);
        } catch (e) {
            return errorParser(e)
        }
    },
    async deleteTask(_, taskId) {
        try {
            await this.$axios.delete(`task/${taskId}/`);
        } catch (e) {
            return errorParser(e)
        }
    },
    async sendStats() {
        try {
            await this.$axios.get('task/send-stats/')
        } catch (e) {
            return errorParser(e)
        }
    }
}