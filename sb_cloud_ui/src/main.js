// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './theme/index.css'
import './assets/css/font-awesome.min.css'
import './assets/css/style.css'
import $ from 'jquery'
import Config from './config/'
import Api from './api/'
import Function from './utils/'
// import hookAjax from 'ajax-hook'

Vue.use(ElementUI);
Vue.prototype.$Api = Api;
Vue.prototype.$Config = Config;
Vue.prototype.$Func = Function;
Vue.config.productionTip = false;
Vue.prototype.$base_url = 'http://127.0.0.1:8000'
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireAuth)) { // 判断该路由是否需要登录权限
    console.log('需要登录',Function.getSessionData('user'));
    if (Function.getSessionData('user')) { // 判断当前的token是否存在 ； 登录存入的token
      if (Function.getSessionData('user').user_token){
        next();
      }else {
        next({
          name: 'Login',
          query: {redirect: to.fullPath} // 将跳转的路由path作为参数，登录成功后跳转到该路由
        })
      }
    }
    else {
      next({
        name: 'Login',
        query: {redirect: to.fullPath} // 将跳转的路由path作为参数，登录成功后跳转到该路由
      })
    }
  }
  else {
    next();
  }
});

$.ajaxSetup({
  contentType: "application/x-www-form-urlencoded;charset=utf-8",
  complete: function (XMLHttpRequest, textStatus) {
    //通过XMLHttpRequest取得响应头，sessionstatus，
    var res = XMLHttpRequest.responseText;
    if (JSON.parse(res).detail != undefined) {
      Function.delSessionData('user');
      Function.delSessionData('families');
      Function.delSessionData('cur_family');
      console.log('此时重登陆')
      Vue.$router.push({
        name: 'Login'
      })
    }
  },
  statusCode:{
    403: function () {
      Function.delSessionData('user');
      Function.delSessionData('families');
      Function.delSessionData('cur_family');
      console.log('此时重登陆status')
      Vue.$router.push({
        name: 'Login'
      })
    }
  }
});
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
});
