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
        showHome: true,
        requireAuth: true,
        showOther: false
      },
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        showHome: false,
        requireAuth: false,
        showOther: true
      },
    },
    {
      path: '/test',
      name: 'test',
      component: resolve => require(['@/views/test/test.vue'], resolve),
      meta: {
        // title: '测试',
        showHome: true,
        requireAuth: true,
        showOther: false
      },
    },
    {
      path: '/register',
      name: 'Register',
      component: resolve => require(['@/views/login/Register.vue'], resolve),
      meta: {
        // title: '注册',
        showHome: false,
        requireAuth: false,
        showOther: true
      },
    },
    {
      path: '/choose_family',
      name: 'ChooseFamily',
      component: resolve => require(['@/views/family/ChooseFamily.vue'], resolve),
      meta: {
        showHome: false,
        requireAuth: true,
        showOther: true
      },
    },
    {
      path: '/add_family',
      name: 'AddFamily',
      component: resolve => require(['@/views/family/AddFamily.vue'], resolve),
      meta: {
        showHome: false,
        requireAuth: true,
        showOther: true
      },
    },
    {
      path: '/account',
      name: 'Account',
      component: resolve => require(['@/views/account/Account.vue'], resolve),
      meta: {
        showHome: true,
        requireAuth: true,
        showOther: false
      },
    },
    {
      path: '/host_list',
      name: 'HostList',
      component: resolve => require(['@/views/host/HostList.vue'], resolve),
      meta: {
        showHome: true,
        requireAuth: true,
        showOther: false
      },
    },
    {
      path: '/disk_list',
      name: 'DiskList',
      component: resolve => require(['@/views/backup/DiskList.vue'], resolve),
      meta: {
        showHome: true,
        requireAuth: true,
        showOther: false
      },
    },
    {
      path: '/snapshot_list',
      name: 'SnapshotList',
      component: resolve => require(['@/views/backup/SnapshotList.vue'], resolve),
      meta: {
        showHome: true,
        requireAuth: true,
        showOther: false
      },
    },
  ]
})
