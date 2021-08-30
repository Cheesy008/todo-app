import {createRouter, createWebHistory} from 'vue-router'
import store from '../store/index';

import Home from '../views/Home.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {requiresAuth: true}
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register')
    },
    {
        path: '/:notFound(.*)',
        component: () => import('../views/NotFound')
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(function (to, _, next) {
    if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
        next('/login');
    } else if ((to.name === 'Login' || to.name === 'Register') && store.getters.isAuthenticated) {
        // если пользователь авторизован, то автоматически перенаправляем его на главную страницу
        // в случае, если он захочет перейти на login/register.
        next('/')
    } else {
        next();
    }
});

export default router
