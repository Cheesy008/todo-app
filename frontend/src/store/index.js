import {createStore} from 'vuex'
import users from './modules/users/index'
import tasks from './modules/tasks/index'

export default createStore({
    modules: {
        users,
        tasks
    }
})
