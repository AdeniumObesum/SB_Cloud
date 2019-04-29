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
        base_url: this.$base_url,
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
          url: app.base_url + '/login/',
          type: 'POST',
          dataType: 'json',
          contentType: 'application/x-www-form-urlencoded',
          data: {email: app.userEmail, password: app.password},
          success: function (data) {
            if (data.code == '0') {
              app.$Func.setSessionData('user', data.data.obj);
              app.$router.push({
                name: 'ChooseFamily'
              })
            }else {
              app.$alert('登录失败，请检查用户名密码', '出错', {
                confirmButtonText: '确定',
                callback: action => {
                  // app.$message({
                  //   type: 'info',
                  //   message: `action: ${ action }`
                  // });
                }
              });
            }
          },
          error: function (XMLHttpRequest, textStatus, errorThrown) {
            app.$alert('未知错误，请检查网络', '出错', {
              confirmButtonText: '确定',
              callback: action => {
              }
            });
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
