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
        :data="snapshotsData"
        ref="table"
        style="width: 100%">
        <el-table-column
          width="200">
          <div slot-scope="scope">
            <div class="linux" style="width: 32px;height: 32px" v-if="scope.row.instance_type_id == 0"></div>
            <div class="windows" style="width: 32px;height: 32px" v-else></div>
            <span>{{scope.row.instance_name}}</span>
            <div>
              <span>公网IP：{{scope.row.pub_ip}}</span>
              <p></p>
              <span>内网IP：{{scope.row.pri_ip}}</span>
            </div>
          </div>
        </el-table-column>
        <el-table-column
          prop="disk_name"
          label="磁盘名">
        </el-table-column>
        <el-table-column
          prop="snapshot_name"
          label="快照名">
        </el-table-column>
        <el-table-column
          prop="source_disk_size"
          label="源磁盘容量(G)">
        </el-table-column>
        <el-table-column
          prop="snapshot_create_time"
          label="创建时间">
          <!--<div slot-scope="scope" style="width: 100%;text-align: center">  传值方式-->
          <!--</div>-->
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          width="150">
          <template slot-scope="scope">
            <span>
              <el-button @click="deleteSnapshot(scope.row.snapshot_id,scope.row.account_id)" type="error" style="transition: .4s;"  :ref="scope.row.id" size="mini">删除</el-button>
            </span>
            <span>
              <el-button @click="" type="warning" style="transition: .4s;"  :ref="scope.row.id" size="mini">回滚</el-button>
            </span>

            <!--<el-button @click="deleteUser(scope.row.id)" v-if="scope.row.active != '0'" type="danger" icon="el-icon-delete" circle size="small"></el-button>-->
            <!--<el-button @click="deleteUser(scope.row.id)" v-else icon="el-icon-check" circle size="small"></el-button>
             v-if="scope.row.status === 0"
              v-else
            -->
          </template>
        </el-table-column>
      </el-table>
      <el-row style="text-align: right;margin-top: 15px">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="total"
          :page-size="perPage"
          @current-change="changePage">
        </el-pagination>
      </el-row>
    </el-container>

  </div>
</template>

<script>
  export default {
    name: "SnapshotList",
    data() {
      return {
        firm_id: '',
        params: {
          name: '',
        },
        cur_firm: {
          firm_key: '',
          firm_name: ''
        },
        cur_family: {},
        user: {},
        firms: [],
        snapshotsData: [],
        allSnapshotData: [],
        total: 0,
        perPage: 3,
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
                app.getSnapshots();
              }
            }
          }
        });

      },
      chooseThisFirm: function (firm_key, firm_name) {
        let app = this;
        app.cur_firm.firm_key = firm_key;
        app.cur_firm.firm_name = firm_name;
        app.getSnapshots();
      },
      getSnapshots: function () {
        let app = this;
        $.ajax({
          url: this.$base_url + '/public_cloud/get_snapshots/',
          type: 'post',
          dataType: 'json',
          data: {user_token: app.user.user_token, family_id: app.cur_family.id,firm_key: app.cur_firm.firm_key},
          success: function (data) {
            if (data.code == 0) {
              app.allSnapshotData = data.data.obj;
              app.snapshotsData = app.allSnapshotData.slice(0,app.perPage);
              app.total = app.allSnapshotData.length;
            }
          }
        });
      },
      changePage: function (curPage) {
        let app = this;
        app.snapshotsData = app.allSnapshotData.slice((curPage-1)*app.perPage,curPage*app.perPage);
      },
      deleteSnapshot: function (snapshotId,accountId) {
        let app = this;
        app.$confirm('确认删除该快照吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(()=>{
          const loading = this.$loading({
            lock: true,
            text: '执行中，请稍后',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          $.ajax({
            url: this.$base_url + '/public_cloud/delete_snapshot/',
            type: 'post',
            dataType: 'json',
            data: {user_token: app.user.user_token,firm_key: app.cur_firm.firm_key,snapshot_id: snapshotId, account_id: accountId},
            success: function (data) {
              loading.close();
              if (data.code == 0) {
                app.$message({
                  type: 'success',
                  message: data.msg,
                  center: true
                });
                app.getSnapshots();
              }else {
                app.$message({
                  type: 'error',
                  message: data.msg,
                  center: true
                })
              }
            }
          });
        }).catch(()=>{
          app.$message({
            type: 'info',
            message: '已取消'
          });
        })
      }
    }
  }
</script>

<style scoped>
  .el-header {
    height: 35px !important;
    border-bottom: 1px #bcbec2 solid;
    /*padding: 0 0 0 0!important;*/
    line-height: 35px;
  }
  .linux {
    background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA4RpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMDY3IDc5LjE1Nzc0NywgMjAxNS8wMy8zMC0yMzo0MDo0MiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDowNzllMWZkYS1kNGNmLWZlNDEtYjE1YS1kYzYxYzA1YTI2YWMiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6RTFEQTFBNUQyMjUwMTFFNkI2QUZFMjNGQkY1QjAwRTAiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6RTFEQTFBNUMyMjUwMTFFNkI2QUZFMjNGQkY1QjAwRTAiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKFdpbmRvd3MpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MTYyZWM5NDQtZjYzMS1kYjQ3LWFmZDUtMDkxMDJjZTk0NjhkIiBzdFJlZjpkb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6ZjcwOTY0OTAtMTdlMC0xMWU2LWJiODctZGU2ODhjMGY2YzZiIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+42UDzQAAA/BJREFUeNrMV29MW1UU/722dK2xwGi3wMIgBowSFKPCIKSDolY2DUtqcF9GplMzHIyFuH3CfTBZwNEEFTWGdcPVMT4IoqxMKl1MQIQMu9jh2MaiWyhZO1YphG7lzyOvz/NK1yzMzbq8+LzJL+/ce85rf++cc8+5l+F5HlIORUNDg2QM6urqGEVEZiT4//CHyyDxUMToqnveq62t/aS1tbV8aWlJaTKZTjY1Ne3TaDRYXFyMGpFeHAKrR3d39/bm5ubqO/OOjo6axMTEEYPB0O73+8X3QGdnZ1RWq1XoOfVtcmGJCaPn3Xi9/FX86uyBxWIpnpqaag8EAlFbo9EoDoGxsbGorNXpMD3H+Z5J9uLQkXW4zS/gzGk/ikq2sF1dXfD5fFFbq9UqDgGWXY4m7lxgCUrV2nFj2gheMNDS/CAOKkO4ePlmdl9fHzweD9mz4obgjitlMgZKpQoTk1Np8+l7cfWXCWQU7sZnbethKCowDAwMFFRUVJz1er2Qy+VwOp3iEGhsPIxQKIT4+HjMzs6kapMSrVsrvoNQRXg1ULyZQqNNAoXglNlsTs/JyQlvBdEIOBwOKBQKCGWb4zi7zWbTJGlWdBwRC3Ec9u8/IGzX9Xq93tbb2/tyMBiMKQQxFSLaZujv70d+fn5lVlbWU2VlZSsZQYTkMhni4uJQVVVFXtBiaGjIODg4mJuSkiIeAbd7EhcuXMLw8Ghl5bs1kcRkBW9EbRISEpC7qSAsW45+uWtkxCleEnpv+PDbFRcZBx/PKygMr4VCHCWlbFVxl4eftu+H1yyyh1Gsf14cD3zU1Aj758bt7h48+nP7OxhyeaFSqcOZLoxloa3MfIzAlTMrBD5NU504/pZ4HsDFVxyK63bjhhzgNfYcsvOexBdf2fD2DkNYHUe99MZ5G47VLMBPUSkqcW1DkjeTVH+IQmDBYzeqtSR4gMw84Mi+W9iwMS2qP9rmQMg1isr3BWPC5WUNN/NBP1CdKkoIJv2ZY9fHgeAMTSaAN8uBs117sWdPNV4ylmL3zlIwt2epKpKNC5hTbOphUz/cIdoueCTbXDQRfLHsWmDzQffs06Pjl+KveW9O72ppseh1unXPWdu+zk1+LOP0T8cVv1+dN73Hppu3yXWlA7H8NlNfX89LdSISjmSSn4j+N0cyXkoCMcX/hG7LPWs7p3/gaZ1ZtfavCDB3X0zojhArgQTCScKzhHOENwhz/0Tgbw63D5UDawiHCC2E1Mizg5DxXyXhj4Q/CfbIXPjkY4RvxCTAr4YQ74juCaE/CQ3xLnuh6Gy837sPSvL79QLmATlQT3AJ/Y9wi7A2khMHHuaax0h9O5a8EP0lwAAszYGGXkCgUwAAAABJRU5ErkJggg==);
  }
  .windows {
    background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA4RpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMDY3IDc5LjE1Nzc0NywgMjAxNS8wMy8zMC0yMzo0MDo0MiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDowNzllMWZkYS1kNGNmLWZlNDEtYjE1YS1kYzYxYzA1YTI2YWMiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6NUFDQjZGNEYyMjUwMTFFNkE1QTE4QTU2N0EwNTg0OEQiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NUFDQjZGNEUyMjUwMTFFNkE1QTE4QTU2N0EwNTg0OEQiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKFdpbmRvd3MpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MTYyZWM5NDQtZjYzMS1kYjQ3LWFmZDUtMDkxMDJjZTk0NjhkIiBzdFJlZjpkb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6ZjcwOTY0OTAtMTdlMC0xMWU2LWJiODctZGU2ODhjMGY2YzZiIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+qAzvpAAAAVBJREFUeNpi/P//P8NAApa2trYBc0FVVRUjC5TNOAD2gz3OxDDAgAWXxCIRD6pZEvdmB+kOIAHwAbEKEKtCMYitDqVFyQ4BNMCFZoEaELcA8XEgFqNJFCCBJ0AsjUW8n1LLiU2E0rRMhAOeC0YdQEwiVMaTOJXp4YC7OMT1gPgSAb2Mo2lgWDjg1UDnAnFohYNe2fwA4rdALExrB4DAJyA+C8XIQASIhZBqQzW0mpFqDsAH3gHxKSgeRiUhvlYMLRzwfyBDgKgWMbY2IjCU/gPFGSkJOUbkjgmwj0CsA/iBeAkQGwLxGSCOB+KPhBwA7AdQJRGyA3EzEM8AYhkovYrcmpEcB+wF4tdAvB3KB3l5DhCvoaYD/qNjUHxD5UClYB8Q/0NSfxCIZXHpxZfIWYitx5HSQCsQn4cWQJ+BWBCaJkrI6eYxDnTveMBLQoAAAwCOJVIaOweJ6QAAAABJRU5ErkJggg==);
  }
</style>
