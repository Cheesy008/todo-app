import mutations from './mutations.js';
import actions from './actions.js';
import getters from './getters.js';

export default {
    namespaced: true,
    state() {
        return {
            tasks: [],
            filterParams: {
                status: '',
                priority: '',
                endDate: ''
            }
        };
    },
    mutations,
    actions,
    getters
};
