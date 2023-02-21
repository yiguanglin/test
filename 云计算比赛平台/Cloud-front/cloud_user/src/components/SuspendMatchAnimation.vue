<template>
  <div class="animation" ref="d">
    <h1>比赛暂停</h1>
  </div>
</template>

<script>
export default {
  data(){
    return{
      animations:false
    }
  },
  watch:{
    animations(val,oldVal){
      if(val === true){
        this.$refs.d.className= "animation tran"
        setTimeout(()=>{
          this.$refs.d.className= "animation"
          this.animations = false
        },3000)
      }
    }
  }
}
</script>

<style scoped lang="less">
.animation{
  width: 100%;
  min-height: 100%;
  // background: rgba(204, 204, 204, 0.244);

  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 9999999;
  z-index: -1;

  display: flex;
  justify-content: center;
  align-items: center;
  h1{
    font-size: 100px;
  }
}

.tran{
  animation: tran 3s linear forwards;
}

@keyframes tran {
  0%{
    opacity: 0;
    z-index: 99999;
  }
  50%{
    opacity: 1;
    z-index: 99999;
  }
  100%{
    opacity: 0;
    display: none;
    z-index: -1;
  }
}
</style>