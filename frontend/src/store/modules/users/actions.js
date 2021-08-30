import errorParser from "../../../utils/errorParser";
import {AuthFormTypes} from "../../../utils/enums";

export default {
    async auth({commit}, payload) {
        let url;
        if (payload['formType'] === AuthFormTypes.LOGIN) {
            url = 'auth/login/'
        } else if (payload['formType'] === AuthFormTypes.REGISTER) {
            url = 'auth/register/'
        } else {
            throw Error('Undefined formType')
        }

        delete payload['formType']

        try {
            const resp = await this.$axios.post(url, payload);

            const token = resp.data.token;
            const user = resp.data.user;

            localStorage.setItem('Token', token);

            commit('SET_TOKEN', token)
            commit('SET_USER', user)
        } catch (e) {
            throw errorParser(e)
        }
    },
    async tryLogin({commit, dispatch}) {
        const token = localStorage.getItem('Token')

        if (token) {
            commit('SET_TOKEN', token)
            await dispatch('fetchUser')
        }
    },
    async logout({commit}) {
        try {
            await this.$axios.post('auth/logout/');
            localStorage.removeItem('Token');
            commit('SET_TOKEN', null)
            commit('SET_USER', null)
        } catch (e) {
            console.log(e)
        }
    },
    async fetchUser({commit}) {
        try {
            const resp = await this.$axios.get('auth/user/');
            commit('SET_USER', resp.data)
        } catch (e) {
            console.log(e)
        }
    },
}