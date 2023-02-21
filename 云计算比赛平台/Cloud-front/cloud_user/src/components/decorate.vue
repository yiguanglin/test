<template>
  <!-- 呼吸灯。。。 -->
  <div class="decorate">
    <div class="decoratey">
      <div v-show="sun>=5"></div>
      <div v-show="sun>=4"></div>
      <div v-show="sun>=3"></div>
      <div v-show="sun>=2"></div>
      <div v-show="sun>=1"></div>
    </div>
    <div class="cont"></div>
    <div class="decoratex">
      <div v-show="sun>=1"></div>
      <div v-show="sun>=2"></div>
      <div v-show="sun>=3"></div>
      <div v-show="sun>=4"></div>
      <div v-show="sun>=5"></div>
    </div>
    <div class="hashcode">
      <i>
        gameID: {{gameId}}
      </i><br>
      <i>
        hashcode: 
        {{hashcode}}
      </i>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return{
      sun:0,
      hashcode:"",
      gameId:""
    }
  },
  mounted(){
    this.hashcode = sessionStorage.getItem('hashcode')
    this.gameId = sessionStorage.getItem('game_id')

    let timer=setInterval(()=>{
      if(this.sun==5){
        // this.sun=0
        clearInterval(timer)
        return
      }
      this.sun++
    },100)
  }
};
</script>

<style scoped lang="less">

.decorate {
  width: 100%;
  position: fixed;
  top: 28px;
  top: 4%;
  left: 0;
  right: 0;
  margin: auto;
  display: flex;
  .cont {
    // border: 1px solid red;
    width: 470px;
    width: 31%;
    height: 10px;
  }
  .decoratex,
  .decoratey {
    flex: 1;
    display: flex;
    div {
      width: 20px;
      height: 30px;
      background: #fff;
      // border: 1px solid #000;
      margin: 0 5px;
      transform: skewX(-42deg);
      &:nth-child(2) {
        opacity: 0.8;
      }
      &:nth-child(3) {
        opacity: 0.6;
      }
      &:nth-child(4) {
        opacity: 0.4;
      }
      &:nth-child(5) {
        opacity: 0.2;
      }
    }
  }
  .decoratey {
    justify-content: flex-end;
    div {
      transform: skewX(42deg);
      &:nth-child(5) {
        opacity: 1;
      }
      &:nth-child(4) {
        opacity: 0.8;
      }
      &:nth-child(3) {
        opacity: 0.6;
      }
      &:nth-child(2) {
        opacity: 0.4;
      }
      &:nth-child(1) {
        opacity: 0.2;
      }
    }
  }

    .hashcode{
    position: fixed;
    top: 5%;
    left: 20px;
    // width: 200px;
    height: 50px;
    // background: #fff;
    
    color: #9c9c9c;
  }
}
</style>