<template>
  <div>
    <el-container>
      <el-header>
        <el-row :gutter="0">
          <el-dropdown>
            <span class="el-dropdown-link" style="color: #409EFF;font-size: 15px; cursor: pointer">
              {{cur_firm.firm_name}}<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <template v-for="item in firms">
                <el-dropdown-item @click="chooseThisFirm(item.firm_key, item.firm_name)">{{item.firm_name}}</el-dropdown-item>
              </template>
            </el-dropdown-menu>
          </el-dropdown>
        </el-row>
      </el-header>
      <el-table
        :data="hostsData"
        ref="table"
        style="width: 100%">
        <el-table-column
          prop="instance_name"
          label="实例名称">
        </el-table-column>
        <el-table-column
          prop="os_name"
          label="系统版本">
        </el-table-column>
        <el-table-column
          prop="instance_type"
          label="系统类型">
        </el-table-column>
        <el-table-column
          prop="instance_status"
          label="状态">
        </el-table-column>
        <el-table-column
          prop="instance_pub_ip"
          label="公网IP">
          <!--<div slot-scope="scope" style="width: 100%;text-align: center">  传值方式-->
          <!--</div>-->
        </el-table-column>
        <el-table-column
          prop="instance_pri_ip"
          label="私有网络IP">
          <!--<div slot-scope="scope" style="width: 100%;text-align: center">{{ $Config.sex[scope.row.sex] }}</div>-->
        </el-table-column>
        <el-table-column
          prop="end_time"
          label="到期时间">
          <!--<div slot-scope="scope" style="width: 100%;text-align: center">-->
          <!--</div>-->
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作">
          <template slot-scope="scope">
            <el-button @click="" type="warning" size="small" v-if="scope.row.status === 0">关机</el-button>
            <el-button @click="" type="primary" style="transition: .4s;"  :ref="scope.row.id" size="small" v-else>开机</el-button>
            <!--<el-button @click="deleteUser(scope.row.id)" v-if="scope.row.active != '0'" type="danger" icon="el-icon-delete" circle size="small"></el-button>-->
            <!--<el-button @click="deleteUser(scope.row.id)" v-else icon="el-icon-check" circle size="small"></el-button>-->
          </template>
        </el-table-column>
      </el-table>
    </el-container>

  </div>


</template>

<script>
  export default {
    name: "HostList",
    data() {
      return {
        firm_id: '',
        params: {
          name: '',
        },
        cur_firm:{
          firm_key: '',
          firm_name: ''
        },
        cur_family: {},
        user: {},
        firms: [],
        hostsData: [
          // {id:1,loginname:'Admin',nickname:'管理员',email:'Admin@.admin.com',cellphone:'151178xxxx',sex:'male',active:1},
          // {id:2,loginname:'SenLin',nickname:'森林',email:'SenLin@.admin.com',cellphone:'151178xxxx',sex:'unknown',active:0},
          // {id:4,loginname:'Admin1',nickname:'赵晓',email:'Admin@.admin.com',cellphone:'151178xxxx',sex:'male',active:1},
          // {id:5,loginname:'Wujun',nickname:'吴军',email:'Admin@.admin.com',cellphone:'151178xxxx',sex:'male',active:1},
          // {id:5,loginname:'Huang',nickname:'黄家',email:'Admin@.admin.com',cellphone:'151178xxxx',sex:'male',active:1},
        ]
      }
    },
    mounted: function () {
      let app = this;
      app.cur_family = app.$Func.getSessionData('cur_family');
      app.user = app.$Func.getSessionData('user');
      app.getFamilyFirms();

    },
    methods: {
      getFamilyFirms: function () {
        let app = this;
        $.ajax({
          url: this.$base_url + '/public_cloud/get_family_firms/',
          type: 'post',
          dataType: 'json',
          data: {user_token: app.user.user_token, family_id: app.cur_family.id},
          success: function (data) {
            if (data.code == 0) {
              app.firms = data.data.obj;
              if (app.firms.length > 0){
                app.cur_firm.firm_key = app.firms[0].firm_key;
                app.cur_firm.firm_name = app.firms[0].firm_name;
                app.getHosts();
              }
            }
          }
        });

      },
      chooseThisFirm: function (firm_key, firm_name) {
        let app = this;
        app.cur_firm.firm_key = firm_key;
        app.cur_firm.firm_name = firm_name;
        app.getHosts();
      },
      getHosts: function () {
        let app = this;
        $.ajax({
          url: this.$base_url + '/public_cloud/get_hosts/',
          type: 'post',
          dataType: 'json',
          data: {user_token: app.user.user_token, family_id: app.cur_family.id,firm_key: app.cur_firm.firm_key},
          success: function (data) {
            if (data.code == 0) {
              app.hostsData = data.data.obj;
            }
          }
        });
      }
    },
    components: {}
  }
</script>

<style scoped>
  .el-header {
    height: 35px !important;
    border-bottom: 1px #bcbec2 solid;
    /*padding: 0 0 0 0!important;*/
    line-height: 35px;
  }
</style>
