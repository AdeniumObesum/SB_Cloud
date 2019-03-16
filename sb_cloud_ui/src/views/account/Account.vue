<template>
    <div>
      <el-row :gutter="0" style="padding-left: 2%;padding-top: 2%;padding-right: 1%">
        <div style="height: 50px;border-bottom: 1px #999999 solid">
          <span>我的Family<span style="color: #666666">（{{families.length}}个）</span></span>
        </div>
        <!--<hr style="margin-top: 30px;color: #e6e6e6">-->
      </el-row>
      <el-row :gutter="30" style="padding-left: 2%; padding-right: 1%">
        <el-col :span="8" v-for="(o, index) in 6">
          <el-card style="margin-top: 30px">
            <div style="padding-left: 35px;font-size: large">
              Family Name
            </div>
            <div style="padding: 0 14px 0 35px;font-size: small">
              <div style="margin-top: 13px">家族拥有者： <span style="color: #999999">{{user.username}}</span></div>
              <div style="margin-top: 13px">云账号数量： <span style="color: #999999">{{user.username}}</span></div>
              <div style="margin-top: 13px">创建时间： <span style="color: #999999">{{user.username}}</span></div>
              <div class="bottom clearfix">
                <el-button type="text" class="button">导入账号</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
</template>

<script>
  export default {
    name: "Account",
    data () {
      return {
        user: this.$Func.getSessionData('user'),
        families: this.$Func.getSessionData('families'),
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
