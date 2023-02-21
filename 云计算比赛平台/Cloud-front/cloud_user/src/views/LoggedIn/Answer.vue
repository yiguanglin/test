<template>
  <div class="answer">
    <div
      @click="answer(i)"
      class="cont"
      v-for="i in subjectData"
      :key="i.id"
    >
      <div class="completed" v-show="complete.indexOf(i.id) != -1">
        <i class="iconfont icon-yiwancheng"></i>
      </div>
      <h3>
        {{
          i.headline
        }}
      </h3>
      <!-- <p>难度:{{i.level}}</p> -->
      <div class="level">
        难度:<i
          class="iconfont icon-nandu"
          v-for="n in i.level"
          :key="n.id"
        ></i>
        <i
          class="iconfont icon-nandu"
          style="color: #ccc"
          v-for="j in 5 - i.level"
          :key="j"
        ></i>
      </div>
      <p>分数:{{ i.grade }}</p>
      <a href="#">开始答题</a>

      <!-- <span class="span1"></span>
      <span class="span2"></span>
      <span class="span3"></span>
      <span class="span4"></span> -->
    </div>

    <answer-win
      @fractionFn="fractionFn"
      ref="answer"
      class="answer"
      @idData="idDataFun"
    ></answer-win>
  </div>
</template>

<script>
import AnswerWin from "@/components/AnswerWin";
export default {
  components: {
    AnswerWin,
  },
  data() {
    return {
      // 存放题目
      subjectData: [
      ],
      // 存放已做完的题目
      complete: [],


      // 请求的数据
      information:{
        token:"",
        hashcode:""
      }
    };
  },
  created() {
    this.information.token = sessionStorage.getItem("token");
    this.information.hashcode = sessionStorage.getItem("hashcode");

    this.subject();
    this.getCompletedTopic()
  },
  methods: {
    // 获取已做完的题目id
    async getCompletedTopic(){
      let {data} = await this.$http.post('/completeID',this.information)
      this.complete = data.data.subject_id
    },


    // 子组件传过来的分数
    fractionFn(vlaue) {
      this.$emit("getFraction", vlaue);
    },

    // 判断 题目是否做完
    answer(value) {
      // for(let i of this.complete){
      //   if(i==value.id){
      //     return this.$message({
      //       message: '本题已提交,无法继续答题',
      //       type: 'warning'
      //     });
      //   }
      // }
      if (this.complete.indexOf(value.id) != -1) {
        return this.$message({
          message: "本题已提交,无法继续答题",
          type: "warning",
        });
      }

      this.$refs.answer.dialogVisible = true;
      this.$refs.answer.subjectData = value;
    },
    // 进来页面时请求数据  获取题目
    async subject() {
      let { data: red } = await this.$http.post("/userSubject", this.information);
      this.subjectData = red.data.subject_list;
    },

    // 题目做完
    idDataFun(value) {
      this.complete.push(value);
    },
  },
};
</script>

<style scoped lang="less">
@import url("~@/css/public.less");

.answer {
  width: 80%;
  width: 1200px;
  margin-top: 50px;
  height: 80vh;
  overflow: auto;
  // overflow: hidden;
  border-radius: 3px;

  display: flex;
  justify-content: wrap;
  align-items: center;
  flex-wrap: wrap;

  // background: #fff;

  position: relative;


  &::-webkit-scrollbar {
    width: 5px;
    background: transparent;
  }
  &::-webkit-scrollbar-thumb {
    background: @light-colour;
    border-radius: 10px;
    width: 5px;
  }

  div.cont {
    width: 260px;
    height: 260px;
    width: 23%;
    margin: 1%;

    // border: 1px solid #fff;
    box-shadow: 0 0px 5px rgba(204, 204, 204, 0.44);
    border-radius: 3px;
    // background: #fff;
    /////////////////////////////////////////////////
    background: url("~@/img/cont.jpg") no-repeat center;
    background-size: 100% 100%;
    // background: #ccc;

    // margin: 18px;
    padding-left: 20px;
    padding-right: 20px;

    color: #9b9b9b;

    position: relative;
    top: 0;

    transition: all 0.3s;
    &:hover {
      position: relative;
      top: -10px;
    }
    h3 {
      font-weight: normal;
      color: #000;
      color: #fff;
      max-height: 50%;
      overflow: hidden;
    }
    a {
      text-decoration: none;
      color: #409eff;
      position: absolute;
      right: 20px;
      bottom: 25px;
    }

    .level {
      i {
        margin: 0 2px;
        color: gold;
        // color: yellow;
      }
    }

    //////////////////////////////////////
    span {
      position: absolute;
      display: inline-block;
      width: 20px;
      height: 20px;
      // background: #fff;
      &.span1 {
        border-top: #8e2de2 5px solid;
        border-left: #8e2de2 5px solid;
        top: -5px;
        left: -5px;
      }
      &.span3 {
        border-right: #8e2de2 5px solid;
        border-bottom: #8e2de2 5px solid;
        right: -5px;
        bottom: -5px;
      }
    }
  }
  // 已完成图
  .completed{
    // width: 50px;
    // height: 50px;
    // width: 100%;
    // height: 100%;
    position: absolute;
    top: 5px;
    right: 0px;
    i{
      font-size: 80px;
      // line-height: 250px;
      text-align: center;
      color: rgb(255, 217, 0);
    }
  }


  .answer {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    margin: auto;
  }
}
</style>