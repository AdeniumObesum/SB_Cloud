<template>
  <div>这是首页</div>

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
