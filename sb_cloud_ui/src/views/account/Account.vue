<template>
  <div>
    <el-row :gutter="0" style="padding-left: 2%;padding-top: 2%;padding-right: 1%">
      <div style="height: 50px;border-bottom: 1px #999999 solid">
        <span>我的Family<span style="color: #666666">（{{families.length}}个）</span></span>
      </div>
      <!--<hr style="margin-top: 30px;color: #e6e6e6">-->
    </el-row>
    <el-row :gutter="30" style="padding-left: 2%; padding-right: 1%">
      <el-col :span="8" v-for="val in families">
        <el-card style="margin-top: 30px">
          <div style="padding-left: 35px;font-size: large">
            {{val.family_name}}
          </div>
          <div style="padding: 0 14px 0 35px;font-size: small">
            <div style="margin-top: 13px">家族拥有者： <span style="color: #999999">{{user.username}}</span></div>
            <div style="margin-top: 13px">云账号数量： <span style="color: #999999">{{val.all_account_count}}</span></div>
            <div style="margin-top: 13px">创建时间： <span style="color: #999999">{{val.create_time}}</span></div>
            <div class="bottom" style="float: left">
              <el-button type="text" class="button" @click="showImport(val.family_id)">导入云主机</el-button>
            </div>
            <div class="bottom clearfix">
              <el-button type="text" class="button" @click="addAccountForm(val.family_id)">导入账号</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!--form-->
    <div>
      <el-dialog title="导入账户" :visible.sync="addAccountFormVisible" center>
        <el-form :model="form_data" ref="form_data" style="padding-left: 17%">
          <el-form-item label="云厂商" label-width="100px"
                        prop="firm_id"
                        :rules="[{required: true, message: '请选择云厂商', trigger: 'blur'}]"
          >
            <el-select v-model="form_data.firm_id" style="width: 60%">
              <template v-for="item in firm_options">
                <el-option :label="item.zh_name" :value="item.firm_key"></el-option>
              </template>
            </el-select>
          </el-form-item>
          <el-form-item label="AccessKey" label-width="100px"
                        prop="access_key"
                        :rules="[{required: true, message: '请填写密钥', trigger: 'blur'}]"
          >
            <el-input v-model="form_data.access_key" autocomplete="" style="width: 60%"></el-input>
          </el-form-item>
          <el-form-item label="SecretKey" label-width="100px"
                        prop="secret_key"
                        :rules="[{required: true, message: '请填写密匙', trigger: 'blur'}]"
          >
            <el-input v-model="form_data.secret_key" autocomplete="" style="width: 60%"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="addAccountFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="addAccount('form_data')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div>
      <el-dialog title="导入云主机" :visible.sync="importHostVisible" center>
        <el-table :data="accountData" stripe max-height="300">
          <el-table-column property="account_id" label="账户" width="100"></el-table-column>
          <el-table-column property="firm_name" label="云厂商" width="120"></el-table-column>
          <el-table-column property="status" label="账户状态" width="120"></el-table-column>
          <el-table-column property="create_date" label="创建日期" width="150"></el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="100">
            <template slot-scope="scope">
              <el-button @click="importHost(scope.row)" type="text" size="small">导入</el-button>
              <el-button type="text" size="small">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-dialog>
    </div>
    <!--form_end-->
  </div>
</template>

<script>
  export default {
    name: "Account",
    data() {
      return {
        addAccountFormVisible: false,
        importHostVisible: false,
        user: {},
        families: [],
        firm_options: [],
        accountData: [],
        form_data: {
          app_id: '',
          firm_id: '',
          family_id: '',
          access_key: '',
          secret_key: ''
        }
      }
    },
    mounted: function () {
      let app = this;
      app.user = app.$Func.getSessionData('user');
      app.getAccounts();
      app.getFirms();
    },
    methods: {
      getAccounts: function () {
        let app = this;
        $.ajax({
          url: app.$base_url + '/public_cloud/get_accounts/',
          type: 'post',
          dataType: 'json',
          data: {user_token: app.user.user_token, user_id: app.user.user_id},
          success: function (data) {
            if (data.code == 0) {
              app.families = data.data.obj;
            }
          }
        })
      },
      getFirms: function () {
        let app = this;
        $.ajax({
          url: app.$base_url + '/public_cloud/get_firms/',
          type: 'post',
          dataType: 'json',
          data: {user_id: app.user.user_id, user_token: app.user.user_token},
          success: function (data) {
            if (data.code == 0) {
              app.firm_options = data.data.obj;
            }
          }
        })
      },
      addAccount: function (formName) {
        let app = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            app.addAccountFormVisible = false;
            $.ajax({
              url: app.$base_url + '/public_cloud/add_account/',
              type: 'post',
              dataType: 'json',
              data: {
                user_token: app.user.user_token,
                app_id: app.form_data.app_id,
                firm_key: app.form_data.firm_id,
                family_id: app.form_data.family_id,
                access_key: app.form_data.access_key,
                secret_key: app.form_data.secret_key
              },
              success: function (data) {
                if (data.code == 0) {
                  // app.families = data.data.obj;
                  app.$notify({
                    title: '提示',
                    message: data.msg,
                    type: 'success',
                    offset: 50
                  });
                  app.getAccounts();
                } else {
                  app.$notify({
                    title: '提示',
                    message: data.msg,
                    type: 'warning',
                    offset: 50
                  });
                }
              },
              error: function () {
                app.$notify({
                  title: '提示',
                  message: '出错了！',
                  type: 'error',
                  offset: 50
                });
              }
            })
          } else {
            return false;
          }
        });
      },
      addAccountForm: function (family_id) {
        let app = this;
        app.form_data.family_id = family_id;
        app.addAccountFormVisible = true;
      },
      showImport: function (family_id) {
        let app = this;
        this.importHostVisible = true;
        $.ajax({
          url: app.$base_url + '/public_cloud/get_account_detail/',
          type: 'post',
          dataType: 'json',
          data: {user_id: app.user.user_id, user_token: app.user.user_token, family_id: family_id},
          success: function (data) {
            if (data.code == 0) {
              app.accountData = data.data.obj;
            }
          }
        })
      },
      importHost: function (data) {
        let app = this;
        const loading = app.$loading({
          lock: true,
          text: '快马加鞭导入中，请稍后',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        $.ajax({
          url: app.$base_url + '/public_cloud/import_host/',
          type: 'post',
          dataType: 'json',
          data: {user_id: app.user.user_id, user_token: app.user.user_token, account_id: data.account_id, firm_key: data.firm_key},
          success: function (data) {
            loading.close();
            if (data.code == 0) {
              app.$notify({
                message: data.msg,
                type: 'success',
                title: '提示',
                offset: 50
              })
            }else {
              app.$notify({
                message: data.msg,
                type: 'error',
                title: '提示',
                offset: 50
              })
            }
          }
        })
      }
    }
  }
</script>

<style scoped>

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both
  }
</style>
