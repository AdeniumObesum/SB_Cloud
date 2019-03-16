<template>
  <div>
    <el-row :gutter="0">
      <el-col :span="12">
        <div class="img">
        </div>
      </el-col>
      <el-col :span="12">
        <div class="contents">
          <el-row :gutter="0">
            <el-col :span="24">
              <el-dropdown style="float: right;margin-right: 20px;margin-top: 10px;cursor: pointer">
                <span class="el-dropdown-link">
                  {{user_name}}<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item @click="logout">注销</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </el-col>
          </el-row>
          <el-row :gutter="0" style="padding-left: 13%;margin-top: 15%">
            <h2 style="font-weight: normal;color: #666666">创建我的Family</h2>
          </el-row>

          <!--<el-row :gutter="0" style="padding-left: 13%;padding-right: 10%;margin-top: 10%">-->
            <!--<span style="color: #8c939d;font-size: 14px;">请选择进入的Family：</span>-->
            <!--<hr style="color: #bbbbbb;margin-top: 10px">-->
          <!--</el-row>-->
          <el-row :gutter="10" style="padding-left: 13%;padding-right: 10%;margin-top: 5%">
            <el-form :model="family_data" ref="family_data">
              <el-form-item
                label="NAME"
                prop="family_name"
                :rules="[
                  { required: true, message: 'Family Name 不能为空'}
                ]"
              ><el-input type="family_name" v-model="family_data.family_name" placeholder="好的名字更容易记住" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="createFamily('family_data')">创建</el-button>
                <el-button @click="resetForm('family_data')">重置</el-button>
              </el-form-item>
            </el-form>
          </el-row>
          <el-row :gutter="0" style="padding-left: 13%;padding-right: 10%;margin-top: 15%">
            <!--你也可以 <span style="font-size: 20px;cursor: pointer;color: #3c8dbc" @click="createFamily">创建新的Family</span>-->
          </el-row>

        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "AddFamily",
    data () {
      return {
        user_name: this.$Func.getSessionData('user').username,
        family_data: {
          family_name: ''
        },
      }
    },
    methods: {
      logout: function () {
        let user_token = this.$Func.getSessionData('user').user_token;
        let app = this;
        $.ajax({
          url: this.$base_url + '/logout/',
          type: 'post',
          dataType: 'json',
          data: {user_token: user_token},
          success: function (data) {
            if (data.code == 0) {
              app.$Func.delSessionData('user');
              app.$router.push({name: 'Login'});
            }
          }
        });
      },
      createFamily(formName) {
        let app = this;
        let user = this.$Func.getSessionData('user');
        this.$refs[formName].validate((valid) => {
          if (valid) {
            $.ajax({
              url: this.$base_url + '/add_family/',
              type: 'post',
              dataType: 'json',
              data: {user_token: user.user_token, user_id: user.user_id, family_name: app.family_data.family_name},
              success: function (data) {
                if (data.code == 0) {
                  app.$router.push({
                    name: 'ChooseFamily'
                  })
                }else {
                  app.$message(data.msg);
                }
              }
            });
          } else {
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>

<style scoped>
  .img {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    right: 50%;
    background-image: url("../../assets/imgs/choose_create_family.jpg");
    /*background-color: #3c8dbc;*/
  }

  .contents {
    position: fixed;
    right: 0;
    top: 0;
    bottom: 0;
    left: 50%;
    background-color: white;
  }
</style>
