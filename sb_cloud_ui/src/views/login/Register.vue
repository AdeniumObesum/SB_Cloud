<template>
  <div class="login">
    <div class="login-form">
      <div class="login-header">
        <!--<img src="../../assets/imgs/logo.svg" width="100" height="100" alt="">-->
        <p>用户注册</p>
      </div>
      <el-input
        placeholder="请输入邮箱"
        suffix-icon="fa fa-user"
        v-model="userEmail"
        style="margin-bottom: 18px"
      >
      </el-input>
      <el-input
        placeholder="请输入昵称"
        suffix-icon="fa fa-user"
        v-model="username"
        style="margin-bottom: 18px"
      >
      </el-input>
      <el-input
        placeholder="请输入手机号"
        suffix-icon="fa fa-user"
        v-model="phoneNum"
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
        @click.native="register"
      >提交
      </el-button>
      <div>
        <!--<el-checkbox v-model="Remember"> Remember</el-checkbox>-->
        <!--<a href="javascript:;" style="float: right;color: #3C8DBC;font-size: 14px">Register</a>-->
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
        username: '',
        phoneNum: '',
        password: '',

        Remember: true,
        loginLoading: false
      }
    },
    methods: {
      register() {
        let app = this;
        app.loginLoading = true;
        $.ajax({
          url:app.$base_url + '/register/',
          // url: 'http://127.0.0.1:8000/login/',
          type: 'POST',
          dataType: 'json',
          contentType: 'application/x-www-form-urlencoded',
          data: {email: app.userEmail, password: app.password, phone: app.phoneNum, username: app.username},
          success: function (data) {

            if (data.code == '0') {
              // 弹窗提示
              app.$message({
                message: '注册成功',
                type: 'success'
              });

              // 1秒后去登录
              setTimeout(function () {
                app.$router.push({
                  name: 'Login'
                })
              },2000);
              app.$router.push({
                name: 'Login',
                params: {}
              });
            } else {
              // 提示失败
              app.$alert(data.msg, '注册失败', {
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
            //提示失败
            app.$alert('未知错误，请检查网络', '出错', {
              confirmButtonText: '确定',
              callback: action => {
                // app.$message({
                //   type: 'info',
                //   message: `action: ${ action }`
                // });
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
