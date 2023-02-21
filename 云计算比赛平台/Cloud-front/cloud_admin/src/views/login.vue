<template>
  <div class="container">
    <el-card>
      <div class="logo">
        <img src="../assets/image/tx.jpeg" alt="" />
      </div>
      <p>云计算实训平台管理员系统</p>
      <el-form
        ref="LoginForm"
        :model="signIn"
        label-width="80px"
        :rules="loginRules"
      >
        <el-form-item label="账号:" class="loginInput" prop="username">
          <el-input v-model="signIn.username"></el-input>
        </el-form-item>
        <el-form-item label="密码:" class="loginInput" prop="password">
          <el-input v-model="signIn.password" show-password></el-input>
        </el-form-item>
        <el-form-item size="large" class="btnLogin">
          <el-button type="primary" class="empty" @click="resetForm">
            重置
          </el-button>
          <el-button type="primary" class="define"  @click="signInHome">
            立即登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
export default {
  data () {
    return {
      signIn: {
        username: '',
        password: ''
      },
      // 表单验证规制
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },
  created () {
    const that = this
    document.onkeydown = function (e) {
      e = window.event || e
      // 验证在登录界面和按得键是回车键enter
      if (that.$route.path === '/login' && (e.code === 'Enter' || e.code === 'enter')) {
      // 登录事件
        that.signInHome()
      }
    }
  },
  methods: {
    signInHome () {
      //  登录前进行表单验证
      this.$refs.LoginForm.validate(async (valid) => {
        if (!valid) return
        // 发请求
        const { data: res } = await this.$http.post('login', this.signIn)
        if (res.status !== 200) {
          return this.$message({
            message: '用户名或者密码错误',
            type: 'error'
          })
        }
        // 验证通过
        this.$message({
          message: '登录成功',
          type: 'success'
        })
        // 保存token
        window.sessionStorage.setItem('username', res.data.username)
        window.sessionStorage.setItem('token', res.data.token)
        // 跳转到hoem页面
        this.$router.push('/home')
      })
    },
    // 重置
    resetForm () {
      this.$refs.LoginForm.resetFields()
    }
  }
}
</script>

<style lang="less" scoped>
.container {
  width: 100%;
  height: 100%;
  background-color: rgb(59,117,95) !important;
  position: relative;
  .el-card {
    background-color: rgba(0,0,0,0) !important;
    width: 450px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    overflow: visible;
    border: none;
    .logo {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      overflow: hidden;
      position: absolute;
      top: -25%;
      left: 50%;
      transform: translateX(-50%);
      &::after {
        content: "";
        display: block;
        clear: both;
      }
      img {
        width: 100%;
        height: 100%;
        opacity: 0.9;
      }

    }
    p{
        margin: 66px 0 20px;
        color: #fff;
        text-align: center;
        font-size: 17px;
      }
    .el-form {
      // margin-top: 77px;
      .btnLogin {
        width: 100%;
        display: flex;
        flex-wrap: nowrap;
        justify-content: flex-end;
        margin-right: 40px;
        .el-button {
          font-size: 10px;
          text-align: center;
          font-weight: bold;
        }
      }
    }
  }
}
</style>
