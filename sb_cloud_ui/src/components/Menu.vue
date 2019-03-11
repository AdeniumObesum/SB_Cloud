<template>
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
  </div>

</template>

<script>
  export default {
    name: "menu",
    data() {
      return {
        isCollapse: true
      }
    },
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>

<style scoped>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
</style>
