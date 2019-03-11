<template>
  <div class="login">
    <div class="login-form">
      <div class="login-header">
        <img src="../../assets/imgs/logo.svg" width="100" height="100" alt="">
        <p>云平台管理</p>
      </div>
      <el-input
        placeholder="请输入邮箱"
        suffix-icon="fa fa-user"
        v-model="userEmail"
        style="margin-bottom: 18px"
      >
      </el-input>

      <el-input
        placeholder="请输入密码"
        suffix-icon="fa fa-keyboard-o"
        v-model="password"
        type="password"
        style="margin-bottom: 18px"
        @keyup.native.enter="login"
      >
      </el-input>


      <el-button
        type="primary" :loading="loginLoading"
        style="width: 100%;margin-bottom: 18px"
        @click.native="login"
      >登录
      </el-button>
      <div>
        <el-checkbox v-model="Remember"> Remember</el-checkbox>
        <router-link :to="{name: 'Register', params: {}}" style="float: right;color: #3C8DBC;font-size: 14px">Register</router-link>
      </div>

    </div>
  </div>
</template>

<script>
  export default {
    name: "Login",
    data() {
      return {
        userEmail: '',
        password: '',
        Remember: true,
        loginLoading: false
      }
    },
    methods: {
      login() {
        let app = this;
        app.loginLoading = true;
        $.ajax({
          url: window.host + '/login/',
          // url: 'http://127.0.0.1:8000/login/',
          type: 'POST',
          dataType: 'json',
          // withCredentials:{
          //
          // },
          contentType: 'application/x-www-form-urlencoded',
          // contentType: 'application/json',
          data: {email: app.userEmail, password: app.password},
          success: function (data) {
            if (data.code == '0') {
              app.$cookieStore.setCookie('user_token', data.data.user.user_token);
              app.$cookieStore.setCookie('user_email', data.data.user.user_email);
              app.$cookieStore.setCookie('is_super', data.data.user.user_token);
              app.$cookieStore.setCookie('username', data.data.user.username);
              app.$cookieStore.setCookie('user_id', data.data.user.user_id);
              // app.$route.meta.keepAlive = true;
              // var tt = app.$cookieStore.getCookie('user_token');
            }else {
              // app.$route.meta.keepAlive = false;
            }
          },
          error: function (XMLHttpRequest, textStatus, errorThrown) {
            app.$route.meta.keepAlive = false;
            console.log(XMLHttpRequest.readyState);
            console.log(textStatus);
            console.log(errorThrown);
          }
        });
        app.loginLoading = false;
      }
    }
  }
</script>

<style lang="less" scoped>
@import "Login";
</style>
