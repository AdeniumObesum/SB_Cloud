<template>
  <div>
    <el-container>
      <el-header>
        <el-row :gutter="0">
          <el-dropdown>
            <span class="el-dropdown-link" style="color: #409EFF;font-size: 15px">
              阿里云<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>阿里云</el-dropdown-item>
              <el-dropdown-item>腾讯云</el-dropdown-item>

            </el-dropdown-menu>
          </el-dropdown>

        </el-row>
      </el-header>
      <el-table
        :data="usersData"
        ref="table"
        style="width: 100%">
        <el-table-column
          prop="loginname"
          label="登录账号">
        </el-table-column>
        <el-table-column
          prop="nickname"
          label="昵称">
        </el-table-column>
        <el-table-column
          prop="email"
          label="邮箱">
        </el-table-column>
        <el-table-column
          prop="cellphone"
          label="手机">
        </el-table-column>
        <el-table-column
          prop="result"
          label="用户体质">
          <div slot-scope="scope" style="width: 100%;text-align: center">{{ scope.row.result ?
            $Config.tizhiCategories[scope.row.result]:'未判定' }}
          </div>
        </el-table-column>
        <el-table-column
          prop="sex"
          width="66"
          label="性别">
          <div slot-scope="scope" style="width: 100%;text-align: center">{{ $Config.sex[scope.row.sex] }}</div>
        </el-table-column>
        <el-table-column
          prop="active"
          width="100"
          label="是否激活">
          <div slot-scope="scope" style="width: 100%;text-align: center">
            <el-tag v-if="scope.row.active">正常</el-tag>
            <el-tag v-else type="danger">被删除</el-tag>
          </div>
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          width="180">
          <template slot-scope="scope">
            <el-button @click="" type="warning" style="transition: .4s;"  :ref="scope.row.id"  icon="el-icon-refresh" size="small" circle></el-button>
            <el-button @click="" type="primary" icon="el-icon-edit" size="small" circle></el-button>
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
        usersData: [
          {id:1,loginname:'Admin',nickname:'管理员',email:'Admin@.admin.com',cellphone:'151178xxxx',sex:'male',active:1},
          {id:2,loginname:'SenLin',nickname:'森林',email:'SenLin@.admin.com',cellphone:'151178xxxx',sex:'unknown',active:0},
          {id:4,loginname:'Admin1',nickname:'赵晓',email:'Admin@.admin.com',cellphone:'151178xxxx',sex:'male',active:1},
          {id:5,loginname:'Wujun',nickname:'吴军',email:'Admin@.admin.com',cellphone:'151178xxxx',sex:'male',active:1},
          {id:5,loginname:'Huang',nickname:'黄家',email:'Admin@.admin.com',cellphone:'151178xxxx',sex:'male',active:1},
        ]
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
