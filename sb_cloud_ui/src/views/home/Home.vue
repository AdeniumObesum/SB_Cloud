<template>
  <div>
    <el-card style="border-radius: 0">
      <div slot="header">
        <span>概况</span>
      </div>
      <div class="demo">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="grid-content">
              <div style="padding: 10px;background: #673AB7">
                <i class="el-icon-location-outline index-icon"></i>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos earum enim fugiat illum iusto minus modi nam natus nisi sequi!
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content ">
              <div style="padding: 10px;background: #3c8dbc">
                <i class="el-icon-picture index-icon"></i>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos earum enim fugiat illum iusto minus modi nam natus nisi sequi!
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content ">
              <div style="padding: 10px;background: #009688">
                <i class="el-icon-service index-icon"></i>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos earum enim fugiat illum iusto minus modi nam natus nisi sequi!
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content ">
              <div style="padding: 10px;background: #607D8B">
                <i class="el-icon-bell index-icon"></i>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos earum enim fugiat illum iusto minus modi nam natus nisi sequi!
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
    <br>
  </div>

</template>

<script>
  export default {
    name: "Home",
    mounted: function () {
      let app = this;
      console.log(app.$Func.getSessionData('cur_family'), 'home session');
      if (app.$Func.getSessionData('cur_family') == undefined) {
        app.$router.push({
          name: 'ChooseFamily'
        })
      }
      // window.location.reload();
    },
    methods: {

    }
  }
</script>

<style scoped>

</style>
