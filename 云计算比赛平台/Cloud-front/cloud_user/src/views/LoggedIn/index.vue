<template>
  <div class="loggedin">
    <h1>云计算挑战平台</h1>

    <!-- 用户名 -->
    <el-dropdown class="name" @command="quits">
      <span class="el-dropdown-link">
        <i class="iconfont icon-yonghu"></i>
        {{ getUserName.username || "未取名"
        }}<span v-if="getUserStatus == 'wating'" class="to-be-reviewed">(待审核)</span
        ><i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="quits">退出</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <!-- 用户积分 -->
    <div class="fraction">积分:{{fraction}}</div>

    <div class="botton" title="排行榜">
      <!-- 排行榜按钮 -->
      <div @click="ranking"><i class="iconfont icon-paixing"></i></div>
      <!-- <div @click="answer"><i class="iconfont icon-dati"></i> 在线答题</div> -->
    </div>

    <!-- 呼吸灯。。。 -->
    <decorate />

    <!-- 题目 -->
    <answer @getFraction="fractionFn" ref="answer"></answer>

    <!-- 弹框 -->
    <el-dialog
      class="set-user-name"
      title="设置用户名"
      :visible.sync="dialogVisibleTan"
      width="30%"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <!-- <span>这是一段信息</span> -->

      <el-input
        v-model="getUserName.username"
        placeholder="请设置用户名"
      ></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submit">提 交</el-button>
      </span>
    </el-dialog>

    <suspend-match-animation ref="suspend"></suspend-match-animation>
  </div>
</template>

<script>
import Answer from "./Answer";

import decorate from "@/components/decorate";

import SuspendMatchAnimation from '@/components/SuspendMatchAnimation'
export default {
  components: {
    Answer,
    decorate,
    SuspendMatchAnimation
  },
  data() {
    return {
      //  响应的用户状态参数
      getUserStatus: "",
      // 编辑用户名的请求参数
      getUserName: {
        id: "",
        token: "",
        username: "",
        hashcode: "",
      },
      gameId:"",
      // 设置用户名窗口 
      dialogVisibleTan: false,
      // 用户分数
      fraction:0,
      // 全局  监听暂停比赛 1 为正在比赛 2 为暂停比赛
      getSuspend:1,
    };
  },
  mounted() {
    this.getUserName.token = window.sessionStorage.getItem("token");
    this.getUserName.id = window.sessionStorage.getItem("id");
    this.getUserName.hashcode = window.sessionStorage.getItem("hashcode");
    this.gameId = window.sessionStorage.getItem("game_id");


    //console.log()

    // this.ToExamine();
    this.viewStatus()
    this.score()

    this.pauseTheGame()
  },
  methods: {
    // 暂停比赛
    pauseTheGame(){
      this.getpauseTheGame = setInterval(async ()=>{
        // console.log(this.$refs.answer.$refs.answer.match)
        // this.$refs.answer.$refs.answer.match = false

        let obj = {
          game_id:this.gameId,
          hashcode:this.getUserName.hashcode,
          token:this.getUserName.token
        }

        let {data} = await this.$http.post('/stopGame',obj)
        
        this.getSuspend = data.data.game_status
      },5000)
    },
    // 接收子组件传来的分数
    fractionFn(value){
      //console.log(value)
      this.fraction = value
    },
    // 获取分数
    async score(){
      let {data} = await this.$http.post("/usergrade",{
        'token':this.getUserName.token,
        'hashcode':this.getUserName.hashcode
      })
      this.fraction = data.data.result
    },
    //用户手动退出登录
    quits(e) {
      //console.log(e);
      this.$confirm("是否要退出登录?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          //清空 本地存储
          sessionStorage.clear()
          this.$router.replace("/");
          this.$message({
            type: "success",
            message: "安全退出",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消",
          });
        });
    },
    //排行榜按钮
    ranking() {
      this.$router.push("/ranking");
    },
    // 确认提交用户名、http
    async submit() {
      if(!this.getUserName.username){
        return this.$message.error('用户名不能为空!');
      }


      // 1. 发请求
      const { data: res } = await this.$http.post(
        "/updateName",
        this.getUserName
      );
      //console.log("提交成功！")
      // 2. 关闭弹框
      this.dialogVisibleTan = false;
      // this.regularView()

      // 改
      this.viewStatus()
    },


    //发送请求  查看状态
    async viewStatus(){
      let {data} = await this.$http.post('/allUser',{
        token: this.getUserName.token,
        hashcode: this.getUserName.hashcode,
      })

      this.getUserName.username = data.data[0].username
      this.getUserStatus = data.data[0].status
      // return data
    },
    //定时请求 查看状态
    regularView(){
      let set = setInterval(async()=>{
        //console.log('正在请求状态...')
        //1. 请求状态
        let {data} = await this.$http.post('/allUser',{
          token: this.getUserName.token,
          hashcode: this.getUserName.hashcode,
        })

        let getSet = data.data[0].status
        // 2. 判断状态
        if(getSet == 'init'){
          //console.log("init")
          clearInterval(set)
        }
        if(getSet == 'wating'){
          //console.log("wating")
        }
        if(getSet == 'noruning'){
          //console.log("noruning")
          clearInterval(set)
        }
        if(getSet == 'runing'){
          //console.log("runing")
          clearInterval(set)
        }
        this.getUserStatus = getSet
      },3000)
    }
  },
  watch: {
    // 判断 用户状态
    getUserStatus(newval, oldval) {
      if (newval == "wating") {
        //待审核
        this.dialogVisibleTan = false;
        this.regularView()

      } else if (newval == "noruning") {
        //驳回
        this.dialogVisibleTan = true;
        
      } else if (newval == "runing") {
        //成功
        this.dialogVisibleTan = false;

      } else if (newval == "init") {
        this.dialogVisibleTan = true;

      }
    },
    getSuspend(newval, oldVal) {
      if(newval == 1){
        this.$refs.answer.$refs.answer.match = false
      }
      if(newval == 2){
        this.$refs.answer.$refs.answer.match = false
        this.$refs.suspend.animations = true
      }
    }
  },
};
</script>

<style scoped lang="less">
@import url('~@/css/public.less');

.loggedin {
  display: flex;
  justify-content: center;
  align-items: center;

  color: #fff;

  width: 100%;
  min-width: 1200px;
  min-height: 100vh;
  background: url("~@/img/interact.png") no-repeat center 0px;
  background-size: cover;
  background-attachment: fixed;
  > h1 {
    margin: 0;
    text-align: center;
    position: fixed;
    top: 1%;
    top: 0;
    left: 0;
    right: 0;
    margin-top: 10px;
  }
  .name {
    position: fixed;
    z-index: 1;
    top: 5%;
    right: 15px;

    color: #fff;
    .icon-yonghu {
      padding: 0 1px;
      font-size: 18px;
      // margin-bottom: -5px;
      position: relative;
      top: 1.8px;
    }
    .to-be-reviewed {
      color: red;
    }
  }

  .fraction {
    position: fixed;
    top: 10%;
    right: 42px;
    right: 10px;
    font-size: 30px;
    font-weight: bold;
    // font-family: "金刚体";
  }

  .botton {
    width: 50px;

    position: fixed;
    right: 30px;
    bottom: 10px;
    margin: auto;
    z-index: 1;

    // display: flex;
    div {
      // border: 1px solid red;
      height: 50px;
      // flex: 1;
      text-align: center;
      cursor: pointer;
      i {
        display: inline-block;
        width: 40px;
        height: 40px;

        line-height: 40px;
        font-size: 30px;
        background: rgb(164, 113, 227);
        border-radius: 5px;

        box-shadow: 2px 2px 5px rgba(204, 204, 204, 0.503);
        position: relative;
        top: 0;
        transition: all 0.3s;
        &:hover {
          box-shadow: 2px 2px 5px rgb(204, 204, 204);
          position: relative;
          top: -10px;
        }
      }
    }
  }

  .set-user-name::v-deep{
    >div{
      background: url('~@/img/cont.jpg') no-repeat center;
      background-size: 100% 100%;
      border: 1px solid @light-colour;
    }
    .el-dialog__title{
      color: #fff;
    }
  }
}
</style>