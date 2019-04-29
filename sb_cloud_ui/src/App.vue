<template>
  <div class="main" id="app">
    <div class="header" v-if="$route.meta.showHome">
      <div class="logo">
        <span class="big">
          <img width="40" style="position: absolute;left: 10px;top: 10px;margin-right: 10px" src="./assets/imgs/云.svg"
               alt="">
        </span>
        <!--<span class="big">{{ siteName }}</span>-->
        <span class="big">云平台管理系统</span>
      </div>
      <span class="header-btn" @click="hiddenSidebar">
        <i class="el-icon-menu"></i>
      </span>
      <div class="right">
        <span class="header-btn" @click="screenfullToggle">
            <i class="fa fa-arrows-alt"></i>
        </span>

        <el-dropdown>
          <span class="header-btn">
               <i class="el-icon-setting"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <div style="padding: 10px;text-align: center;width: 420px">
              <div class="setting-category" style="display: flex;height: 80px;align-items: center">
                <div style="width: 80px">
                  <el-button type="primary" icon="el-icon-sort" circle @click="ToggleGrayMode"
                             style="transform: rotate(90deg)"></el-button>
                </div>
                <div style="flex: 1;margin-top: -8px">
                  <el-alert
                    style="margin-top: 10px"
                    title="切换灰度模式!"
                    type="info"
                    show-icon>
                  </el-alert>
                </div>
              </div>
              <!--<div class="setting-category">-->
              <!--下个设置块-->
              <!--</div>-->

            </div>
          </el-dropdown-menu>
        </el-dropdown>

        <!--<span class="header-btn">-->
        <!--<el-badge :value="3" class="badge">-->
        <!--<i class="el-icon-bell"></i>-->
        <!--</el-badge>-->
        <!--</span>-->
        <!--家族选项-->
        <el-dropdown>
          <span class="header-btn">
              {{currentFamily.name}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <template v-for="item in families">
              <div style="" @click="toFamily(item.id, item.family_name)">
                <el-dropdown-item><i style="padding-right: 8px" class="fa fa-key"></i>
                  <span>{{item.family_name}}</span>
                </el-dropdown-item>
              </div>
            </template>
            <div @click="toAddFamily">
              <el-dropdown-item><span style="padding-left: 15px">创建❤家族</span></el-dropdown-item>
            </div>

          </el-dropdown-menu>
        </el-dropdown>
        <!--end家族-->
        <el-dropdown>
          <span class="header-btn">
            {{curUser.username}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native="$router.push('/personal')"><i style="padding-right: 8px"
                                                                           class="fa fa-cog"></i>个人中心
            </el-dropdown-item>
            <el-dropdown-item @click.native="logout"><i style="padding-right: 8px" class="fa fa-key"></i>退出系统
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <div class="app" v-if="$route.meta.showHome">
      <div class="aside">
        <div class="menu">
          <el-menu
            router
            background-color="#222d32"
            text-color="#fff"
            :default-active="$route.path" class="menu" @open="handleOpen" @close="handleClose"
            :collapse="isCollapse">
            <template v-for="(menu_v,menu_k) in menu">
              <el-submenu v-if="menu_v.children" :index="menu_k">
                <template slot="title">
                  <i :class="menu_v.icon"></i>
                  <span slot="title">{{ menu_v.name }}</span>
                </template>
                <el-menu-item v-for="(menuChildren_v,menuChildren_k) in menu_v.children"
                              :key="menuChildren_k"
                              :index="menuChildren_v.path">
                  <i class="is-children fa fa-circle-o"></i>
                  <span slot="title">{{ menuChildren_v.name }}</span>
                </el-menu-item>
              </el-submenu>
              <el-menu-item v-else :index="menu_v.path">
                <i :class="menu_v.icon"></i>
                <span slot="title">{{ menu_v.name }}</span>
              </el-menu-item>
            </template>
          </el-menu>
        </div>
        <div class="sidebar-toggle" @click="sidebarToggle">
          <div class="icon-left">
            <i class="el-icon-back"></i>
          </div>
        </div>
      </div>
      <div class="app-body">
        <div style="margin-top: 50px;"></div>
        <div id="mainContainer" class="main-container">
          <!--<transition name="fade">-->
          <router-view></router-view>
          <!--</transition>-->
        </div>
        <EuiFooter></EuiFooter>
      </div>
    </div>

    <!--登录-->
    <div v-if="$route.meta.showOther && !$route.meta.requireAuth">
      <router-view></router-view>
    </div>

    <!--选择家族 或者 创建家族-->
    <div v-if="$route.meta.showOther">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  import Screenfull from 'screenfull'
  import EuiFooter from './components/Footer.vue';
  import NavBar from './components/NavBar.vue'
  import Menu from '@/menu/index';
  import $ from 'jquery'

  export default {
    data() {
      return {
        siteName: '云平台管理系统',
        isCollapse: false,
        menu: Menu,
        curUser: this.$Func.getSessionData('user'),
        currentFamily: this.$Func.getSessionData('cur_family'),
        families: this.$Func.getSessionData('families')
      };
    },
    methods: {
      NavBarWidth() {
        let navBar = document.getElementById('nav-bar');
        if (!navBar) return;
        let sidebarClose = document.body.classList.contains('sidebar-close');
        if (sidebarClose) {
          navBar.style.width = '100%';
          return;
        }
        if (this.isCollapse) navBar.style.width = 'calc(100% - 64px)';
        else navBar.style.width = 'calc(100% - 230px)';

      },
      ToggleGrayMode() {
        document.body.classList.toggle("gray-mode")
      },
      screenfullToggle() {
        if (!Screenfull.enabled) {
          this.$message({
            message: '你的浏览器不支持全屏！',
            type: 'warning'
          });
          return false
        }
        Screenfull.toggle();
      },
      sidebarToggle(e) {
        e.preventDefault();
        if (this.isCollapse) {
          document.body.classList.remove('sidebar-hidden');
          this.siteName = this.$Config.siteName;
          this.isCollapse = false;
        } else {
          document.body.classList.add('sidebar-hidden');
          this.isCollapse = true;
        }
        this.NavBarWidth();

      },
      hiddenSidebar(e) {
        e.preventDefault();
        document.body.classList.toggle('sidebar-close');
        this.NavBarWidth();
      },
      logout() {
        let user_token = this.$Func.getSessionData('user').user_token;
        console.log(user_token);
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
      handleOpen(key, keyPath) {
        //console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        //关闭菜单
      },
      toFamily: function (cur_family_id,cur_family_name) {
        let app = this;
        let cur_family = {
          id: cur_family_id,
          name: cur_family_name
        };
        app.$Func.setSessionData('cur_family', cur_family);
        app.currentFamily = cur_family;
        window.location.reload();
      },
      toAddFamily: function () {
        let app = this;
        app.$router.push({
          name: 'AddFamily'
        })
      }
    },
    watch: {
      '$route': function () {
        let app = this;
        console.log('路由变化');
        app.currentFamily = app.$Func.getSessionData('cur_family');
      }

    },
    mounted: function () {
      let app = this;
      if (!this.isCollapse) {

        document.body.classList.remove('sidebar-hidden')
        // this.siteName = this.$Config.siteName
      } else {
        document.body.classList.add('sidebar-hidden')
      }

      setTimeout(() => {
        this.NavBarWidth();
      }, 1000);
      // if (app.currentFamily == undefined){
      //   app.$router.push({
      //     name: 'ChooseFamily'
      //   })
      // }else {
      //   app.currentFamily = app.$Func.getSessionData('cur_family')
      // }
    },
    components: {
      EuiFooter, NavBar
    },

  }
</script>
<style lang="less">

  .sidebar-hidden {
    .header {
      .logo {
        background: #222d32;
        .big {
          display: none;
        }
        .min {
          display: block;
        }
        width: 64px;
      }

    }
    .aside {
      .sidebar-toggle {
        .icon-left {
          transform: rotate(180deg);
        }
      }
    }
    .main {
      .app-body {
        margin-left: 64px;
      }
    }
  }

  .sidebar-close {
    .header {
      .logo {
        width: 0;
        overflow: hidden;
        position: relative;
      }
    }
    .aside {
      margin-left: -230px;
    }
    .main {
      .app-body {
        margin-left: 0;
      }
    }
  }

  .sidebar-hidden.sidebar-close {
    .aside {
      margin-left: -64px;
    }
  }

  .main {
    display: flex;
    .el-menu:not(.el-menu--collapse) {
      width: 230px;
    }
    .app {
      width: 100%;
      background-color: #ecf0f5;
    }
    .aside {
      position: fixed;
      margin-top: 50px;
      z-index: 10;
      background-color: #222d32;
      transition: all 0.3s ease-in-out;
      .menu {
        overflow-y: auto;
        height: calc(~'100vh - 100px');
      }
      .sidebar-toggle {
        position: relative;
        width: 100%;
        height: 50px;
        background-color: #367fa9;
        color: #fff;
        cursor: pointer;
        .icon-left {
          position: absolute;
          display: flex;
          align-items: center;
          justify-content: center;
          right: 0;
          width: 64px;
          height: 100%;
          font-size: 20px;
          transition: all 0.3s ease-in-out;
        }
      }
    }
    .app-body {
      margin-left: 230px;
      -webkit-transition: margin-left 0.3s ease-in-out;
      transition: margin-left 0.3s ease-in-out;
    }
    .main-container {
      //margin-top: 50px;
      padding: 6px;
      min-height: calc(~'100vh - 101px');
    }
  }

  .header {
    width: 100%;
    position: fixed;
    display: flex;
    height: 50px;
    background-color: #3c8dbc;
    z-index: 10;
    .logo {
      .min {
        display: none;
      }
      width: 230px;
      height: 50px;
      text-align: center;
      line-height: 50px;
      color: #fff;
      background-color: #367fa9;
      -webkit-transition: width 0.35s;
      transition: all 0.3s ease-in-out;
    }
    .right {
      position: absolute;
      right: 0;
    }
    .header-btn {
      .el-badge__content {
        top: 14px;
        right: 7px;
        text-align: center;
        font-size: 9px;
        padding: 0 3px;
        background-color: #00a65a;
        color: #fff;
        border: none;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: .25em;
      }
      overflow: hidden;
      height: 50px;
      display: inline-block;
      text-align: center;
      line-height: 50px;
      cursor: pointer;
      padding: 0 14px;
      color: #fff;
      &:hover {
        background-color: #367fa9
      }
    }

  }

  .menu {
    border-right: none;
  }

  .el-menu--vertical {
    min-width: 190px;
  }

  .setting-category {
    padding: 10px 0;
    border-bottom: 1px solid #eee;
  }
</style>
