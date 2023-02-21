<template>
  <div class="home">
    <div class="input-box">
      <div class="cont"></div>
      <div class="contt"></div>
      <div class="conttt"></div>
      <div class="input-b">
        <h1>云计算挑战平台</h1>
        <div class="d1" :class="{'d1s':input}">
          <span class="iconfont icon-mima" :style="input?'color:#fff;':''"></span>
          <input
            @keyup.enter="submit"
            v-model="input"
            type="text"
            placeholder="请输入Hashcode"
          />
        </div>
        <div class="d2" @click="submit">
          登录<i class="iconfont icon-queding"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      input: "",
      // msg: {
      //   hashcode: "af470646a106d84a",
      // },
    };
  },
  components: {},
  methods: {
    //登录提交
    async submit() {
      if (!this.input) {
        return this.$message({
          message: "Hashcode不能为空!",
          type: "warning",
        });
      }
      const { data: res } = await this.$http.post("login", {
        hashcode: this.input,
      })
      if (res.status !== 200) {
        return this.$message({
          message: "Hashcode错误",
          type: "warning",
        });
      }
      if (res.msg == "比赛未开始!"){
        return this.$message({
          message: "比赛未开始!",
          type: "warning",
        });
      }
      // 登录成功
      this.$message({
        message: "登录成功!",
        type: "success",
      });
      sessionStorage.setItem("token", res.data.token);
      sessionStorage.setItem("id", res.data.id);
      sessionStorage.setItem("hashcode", res.data.hashcode);
      sessionStorage.setItem("game_id", res.data.game_id);

      this.$router.replace("/loggedin");
    },
  },

  created(){
    ////console.log("创建后")
  }
};
</script>

<style scoped lang="less">
.public {
  width: 650px;
  height: 650px;
  background-size: 115%;
}

.home {
  display: flex;
  justify-content: center;
  align-items: center;

  width: 100%;
  min-width: 800px;
  min-height: 100vh;

  background: linear-gradient(90deg, #000046, #1cb5e0);
  background: url("~@/img/homeBack.jpg") no-repeat;
  background-size: cover;

  .input-box {
    overflow: hidden;
    background: url("~@/img/animation/1.png") no-repeat center;
    border-radius: 50%;
    .public;

    position: relative;
    .cont {
      background: url("~@/img/animation/2.png") no-repeat center;
      .public;

      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      margin: auto;

      animation: zhuan 8s infinite linear;
    }
    .contt {
      background: url("~@/img/animation/3.png") no-repeat center;
      .public;

      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      margin: auto;

      animation: zhuana 8s infinite linear;
    }
    .conttt {
      background: url("~@/img/animation/4.png") no-repeat center;
      .public;

      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      margin: auto;

      animation: zhuan 8s infinite linear;
    }
    .input-b {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      margin: auto;
      // z-index: -1;

      width: 363px;
      height: 363px;
      // border: 1px solid red;
      border-radius: 50%;
      background: #5d84aa6d;

      display: flex;
      flex-direction: column;
      flex-wrap: nowrap;
      justify-content: center;
      align-items: center;
      .d1,
      .d2,
      .d1s,
      h1 {
        // margin: 0;
        text-align: center;
        width: 250px;
        height: 50px;
        // border: 1px solid red;
        // margin: 15px 0;
        color: #fff;
      }
      h1 {
        text-shadow: 0px 2px 3px #ccc;
        margin-bottom: 30px;
        font-size: 35px;
      }
      .d1 {
        background: url("~@/img/animation/5.png") no-repeat center -258px;
        background-size: 245%;
        display: flex;
        span {
          flex: 1;
          font-size: 20px;
          line-height: 52px;
          color: #999;
        }
        input {
          background: rgba(255, 255, 255, 0);
          width: 180.2px;
          border: 0;
          padding-left: 10px;
          outline: none;
          color: #fff;
          &::-webkit-input-placeholder {
            color: #999;
          }
        }
      }
      .d1s {
        background: url("~@/img/animation/inputbox.png") no-repeat center -11px;
        background-size: 113%;
        display: flex;
        span {
          flex: 1;
          font-size: 20px;
          line-height: 52px;
          color: #999;
        }
        input {
          background: rgba(255, 255, 255, 0);
          width: 180.2px;
          border: 0;
          padding-left: 10px;
          outline: none;
          color: #fff;
          &::-webkit-input-placeholder {
            color: #999;
          }
        }
      }
      .d2 {
        background: url("~@/img/animation/5.png") no-repeat center -318px;
        background-size: 242%;
        line-height: 52px;
        cursor: pointer;
        position: relative;
        i {
          position: absolute;
          right: 20px;
        }
      }
    }
  }
}

@keyframes zhuan {
  0% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(180deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
@keyframes zhuana {
  0% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(-180deg);
  }
  100% {
    transform: rotate(-360deg);
  }
}
</style>