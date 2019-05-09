<template>
  <div>
    <el-card style="border-radius: 0">
      <div slot="header">
        <span style="color: #666666">欢迎使用云平台管理系统</span>
      </div>
      <div style="width: 100%;height: 80px">
        <span style="color:#6f7180;font-size: small">跨云-多账号-统一化管理</span>
      </div>
      <div class="demo">
        <!--<el-row :gutter="20">-->
          <!--<el-col :span="12">-->
            <!--<div class="grid-content">-->
              <!--<div id="accounts" style="padding: 10px;background: #C1C4FC;width: 100%;height: 320px"></div>-->
            <!--</div>-->
          <!--</el-col>-->
          <!--<el-col :span="12">-->
            <!--<div class="grid-content ">-->
              <!--<div id="hosts" style="padding: 10px;background: #C1C4FC;width: 100%;height: 320px">-->
              <!--</div>-->
            <!--</div>-->
          <!--</el-col>-->
        <!--</el-row>-->
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
      // app.drawPieAccount();
      // app.drawPieHost();

      // window.location.reload();
    },
    methods: {
      drawPieAccount: function () {
        let app = this;
        let myChart = app.$echarts.init(document.getElementById('accounts'));
        let option = {
          tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
          },
          legend: {
            orient: 'vertical',
            x: 'left',
            data:['阿里云']
          },
          series: [
            {
              name:'云账户',
              type:'pie',
              // radius: ['50%', '70%'],
              avoidLabelOverlap: false,
              label: {
                normal: {
                  show: false,
                  position: 'center'
                },
                emphasis: {
                  show: true,
                  textStyle: {
                    fontSize: '30',
                    fontWeight: 'bold'
                  }
                }
              },
              labelLine: {
                normal: {
                  show: false
                }
              },
              data:[
                {value:335, name:'阿里云'},
              ]
            }
          ]
        };

        myChart.setOption(option);
      },
      drawPieHost: function () {
        let app = this;
        let myChart = app.$echarts.init(document.getElementById('hosts'));
        let option = {
          tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
          },
          legend: {
            orient: 'vertical',
            x: 'left',
            data:['阿里云']
          },
          series: [
            {
              name:'云账户',
              type:'pie',
              // radius: ['50%', '70%'],
              avoidLabelOverlap: false,
              label: {
                normal: {
                  show: false,
                  position: 'center'
                },
                emphasis: {
                  show: true,
                  textStyle: {
                    fontSize: '30',
                    fontWeight: 'bold'
                  }
                }
              },
              labelLine: {
                normal: {
                  show: false
                }
              },
              data:[
                {value:335, name:'阿里云'},
              ]
            }
          ]
        };

        myChart.setOption(option);
      },
    }
  }
</script>

<style scoped>
/*a {*/
  /*color: ;*/
/*}*/
  .demo {
    height: 320px;
  }
</style>
