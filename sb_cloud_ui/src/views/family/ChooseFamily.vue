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
          <el-row :gutter="0" style="padding-left: 13%">
            <h2 style="font-weight: normal;color: #666666">欢迎使用公有云管理平台</h2>
          </el-row>

          <el-row :gutter="0" style="padding-left: 13%;padding-right: 10%;margin-top: 10%">
            <span style="color: #8c939d;font-size: 14px;">请选择进入的Family：</span>
            <hr style="color: #bbbbbb;margin-top: 10px">
          </el-row>
          <el-row :gutter="10" style="padding-left: 13%;padding-right: 10%;margin-top: 5%">
            <template v-for="item in families">
            <el-col :span="5">
              <div style="display: inline-block" @click="toFamily(item.id, item.family_name)">
                <el-card shadow="hover" style="margin-top: 15px;cursor: pointer;height: 60px">
                  <!--family{{ val }}-->
                  {{item.family_name}}
                </el-card>
              </div>
            </el-col>
            </template>
          </el-row>
          <el-row :gutter="0" style="padding-left: 13%;padding-right: 10%;margin-top: 15%">
            你也可以 <span style="font-size: 20px;cursor: pointer;color: #3c8dbc" @click="createFamily">创建新的Family</span>
          </el-row>

        </div>
        <!--<img src="../../assets/imgs/choose_create_family.jpg" style="height: auto;width: auto" alt="">-->
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "ChooseFamily",
    data() {
      return {
        user_name: this.$Func.getSessionData('user').username,
        families: [],
      }
    },
    mounted: function () {
      let app = this;
      app.getAllFamilies();
    },
    methods: {
      getAllFamilies: function () {
        let user = this.$Func.getSessionData('user');
        let app = this;
        $.ajax({
          url: this.$base_url + '/public_cloud/get_families/',
          type: 'post',
          dataType: 'json',
          data: {user_token: user.user_token, user_id: user.user_id},
          success: function (data) {
            if (data.code == 0) {
              app.families = data.data.obj;
              app.$Func.setSessionData('families', data.data.obj);
            }
          }
        });
      },
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
      toFamily: function (cur_family_id,cur_family_name) {
        let app = this;
        let cur_family = {
          id: cur_family_id,
          name: cur_family_name
        };
        app.$Func.setSessionData('cur_family', cur_family);
        app.$router.push({
          name: 'Home'
        });
      },
      createFamily: function () {
        let app = this;
        app.$router.push({
          name: 'AddFamily',
        });
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
