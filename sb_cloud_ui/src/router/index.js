import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Login from '@/views/login/Login'
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: resolve => require(['@/views/home/Home.vue'], resolve),
      meta: {
        keepAlive: true,
        requireAuth: true
      },
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        keepAlive: false,
        requireAuth: false
      },
    },
    {
      path: '/test',
      name: 'test',
      component: resolve => require(['@/views/test/test.vue'], resolve),
      meta: {
        title: '测试',
        keepAlive: true,
        requireAuth: true
      },
    },
    {
      path: '/register',
      name: 'Register',
      component: resolve => require(['@/views/login/Register.vue'], resolve),
      meta: {
        title: '注册',
        keepAlive: false,
        requireAuth: false
      },
    }
  ]
})
