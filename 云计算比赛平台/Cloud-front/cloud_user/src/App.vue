<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>

export default ({
  data(){
    return{
      getMatch:true
    }
  },
  beforeCreate(){
    document.addEventListener('contextmenu',function(e){
      e.preventDefault()
    })
    document.addEventListener('selectstart',function(e){
      e.preventDefault()
    })
    document.addEventListener('keydown',e=>{
      if(e.code === "F12"){
        e.preventDefault()
      }
    })
  }
})
</script>


<style lang="less">
@import url('~@/css/normalize.css');
@import url('http://at.alicdn.com/t/font_3388459_8339jhyjupe.css');//阿里
// @import url('~@/font/ali/iconfont.css');

// @font-face {
//   font-family: '金刚体';
//   src: url('~@/font/创客贴金刚体.otf');
// }
*{
  box-sizing: border-box;
  font-family: '微软雅黑','宋体';
}
</style>
