<template>
  <!-- 题目界面 -->
  <el-dialog
    :title="subjectData.headline"
    :visible.sync="dialogVisible"
    width="60%"
    class="dialog"
    :before-close="handleClose"
    :modal="false"
  >
    <!-- 题目内容 -->
    <div v-html="subjectData.text" class="subjectData"></div>
    <!-- 输入框 -->
    <el-input v-model="submitData.answer" placeholder="请输入答案"></el-input>
    <span slot="footer" class="dialog-footer">
      <el-button
        type="success"
        @click="(dialogVisible = false), (submitData.answer = '')"
        >取 消</el-button
      >
      <el-button type="primary" @click="submit" :disabled="!match"
        >提 交</el-button
      >
    </span>
  </el-dialog>
</template>

<script>
export default {
  // name:AnswerWin,
  data() {
    return {
      // 是否显示
      dialogVisible: false,
      // 题目信息
      subjectData: {
        answer: "",
        grade: 0,
        headline: "",
        id: "",
        level: 0,
        text: "",
        url: "",
      },
      // 存放提交请求参数
      submitData: {
        id: "", //题目id
        user_id: "", //用户id
        game_id: "", //比赛ID
        answer: "", //正确答案
        grade: "", //题目分数
        hashcode: "",
        token: "",
        headline: "", //题目标题
      },

      // 暂停比赛  禁用提交按钮  true为可答题
      match: true,
    };
  },
  beforeUpdate() {
    this.submitData.user_id = sessionStorage.getItem("id");
    this.submitData.hashcode = sessionStorage.getItem("hashcode");
    this.submitData.token = sessionStorage.getItem("token");
    this.submitData.game_id = sessionStorage.getItem("game_id");
    this.submitData.id = this.subjectData.id;
    this.submitData.grade = this.subjectData.grade;
    this.submitData.headline = this.subjectData.headline;
  },
  methods: {
    handleClose(done) {
      // this.subjectData = {};
      this.submitData.answer = "";
      done();
    },
    // 提交答案
    async submit() {
      if (!this.submitData.answer) {
        return this.$message.error("答案不能为空");
      }

      let { data } = await this.$http.post("post_answer", this.submitData);
      // console.log(data)

      if (data.status == 200) {
        // //console.log(data.data.result)
        let fraction = data.data.result;
        this.$emit("fractionFn", fraction); //分数 传给父组件

        this.$emit("idData", this.subjectData.id); //返回已做完id

        this.$message({
          type: "success",
          message: "提交答案正确!",
        });
      } else {
        this.$message.error("提交答案错误!");
      }

      this.dialogVisible = false; //关闭窗口
      this.submitData.answer = ""; //清空输入框
    },
  },
  watch: {
    subjectData(val, oldVal) {
      this.submitData.id = val.id;
      this.submitData.grade = val.grade;
    },
  },
};
</script>

<style scoped lang="less">
@import url("~@/css/public.less");
div.dialog::v-deep {
  // min-height: 500px;
  // padding-top: 100px;
  > div {
    // background: #000 !important;
    // box-shadow: 0px 0px 5px #fff;
    border: 2px solid @light-colour;
    background: url("~@/img/cont.jpg") no-repeat center;
    background-size: 100% 100%;
  }
  div,
  span {
    color: #fff;
  }

  .subjectData {
    width: 100%;
    margin-bottom: 20px;
    color: #fff;
    img {
      width: 100%;
      height: 100%;
    }
    a {
      color: #43b6f8;
    }
  }
  // .cancel{

  //   span{

  //   }
  // }
}
.dialog::-webkit-scrollbar {
  width: 0;
  height: 0;
  background: transparent;
  // overflow: hidden;
}

// .subjectData{
//   width: 100%;
//   overflow: hidden;
//   img{
//     width: 100%;height: 100%;
//   }
// }
</style>