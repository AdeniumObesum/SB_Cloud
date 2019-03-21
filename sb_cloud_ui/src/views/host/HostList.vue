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
      <div>主机列表</div>
    </el-container>

  </div>


</template>

<script>
  export default {
    name: "HostList",
    data() {
      return {
        firm_id: '',
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
