<template>
  <el-dialog
    title="设置用户名"
    :visible.sync="tan"
    width="30%"
    class="dialog"
    :before-close="handleClose"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <!-- <span>这是一段信息</span> -->

    <el-input v-model="input" placeholder="请设置用户名"></el-input>
    <span slot="footer" class="dialog-footer">
      <el-button type="primary" @click="submit">提 交</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  data() {
    return {
      input: "",
      tan: true,
    };
  },
  methods: {
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },

    // 提交判断是否为空
    async submit() {
      if (!this.input) {
        this.$message({
          message: "用户名不能为空!",
          type: "warning",
        });
      } else {
        this.tan = false;
        // this.username=this.input

        this.$message({
          message: "用户设置成功,等待管理员确定",
          type: "success",
        });

        this.$emit("name", this.input);

        /////////////////////////////////////////////////////////////////
        sessionStorage.setItem("username", this.input);
        sessionStorage.setItem("ToExamine", true);

        //console.log("用户名设置成功");
        let token = sessionStorage.getItem("token");
        let id = sessionStorage.getItem("id");
        const { data: res } = await this.$http.post("updateName", {
          id: id,
          username: this.input,
          token: token,
        });
        //console.log(res);
        // this.$router.go(0)
      }
    },
    quits(e) {
      //console.log(e);
      this.$router.replace("/");
    },

    ////////////////////////////
    ranking() {
      // //console.log("排行榜")
      if (this.tan) {
        this.$message({
          message: "请先设置用户名",
          type: "warning",
        });
        return;
      }
      //console.log("排行榜");
    },
    answer() {
      // //console.log("答题")
      if (this.tan) {
        this.$message({
          message: "请先设置用户名",
          type: "warning",
        });
        return;
      }
      //console.log("答题");
    },
  },
  created() {
    // //console.log("创建后");
    // sessionStorage.getItem(key)
    if (sessionStorage.getItem("username") != null) {
      this.tan = false;
    }
  },
};
</script>
