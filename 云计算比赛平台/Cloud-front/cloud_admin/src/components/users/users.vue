<template>
  <div>
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/users' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>生成HASH</el-breadcrumb-item>
      </el-breadcrumb>
      <!-- 生成hash和比赛选手 -->
      <el-form
        ref="userFormRef"
        :model="userForm"
        label-width="80px"
        :rules="userRules"
      >
        <el-row>
          <el-col :span="6"
            ><el-form-item label="比赛名称" prop="gamename">
              <el-input v-model="userForm.gamename"></el-input> </el-form-item
          ></el-col>
          <el-col :span="6">
            <el-form-item label="比赛人数" prop="num">
              <el-input v-model="userForm.num"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="9"
            ><el-form-item>
              <el-button
                @click="resetUserForm('userFormRef')"
                class="btn empty"
                type="danger"
                icon="el-icon-delete"
                >清空</el-button
              >
              <el-button @click="submitUserForm" type="primary" class="btn define"
                >生成</el-button
              >
            </el-form-item></el-col
          >
        </el-row>
      </el-form>
      <!-- 搜索比赛 -->
      <el-form
        ref="searchGameRef"
        :model="searchGame"
        label-width="80px"
        :rules="userRules">
        <el-col :span="5">
            <el-form-item label="搜索比赛" prop="game_id" >
              <el-input v-model="searchGame.game_id" placeholder="请输入比赛ID"></el-input>
            </el-form-item>
          </el-col>
        <el-col :span="1">
         <el-form-item>
            <el-button  type="primary" class="btn define" @click="searchGameHash">搜索</el-button>
          </el-form-item>
        </el-col>
      </el-form>
      <!-- 显示hash列表 -->
      <div id="export">
        <el-table
          :data="HashData"
          height="250"
          border
          style="width: 100%"
          ref="HashTable"
        >
         <el-table-column
        label="#"
      type="index"
      :index="1">
    </el-table-column>
          <el-table-column prop="game_name" label="比赛名称"> </el-table-column>

          <el-table-column prop="hash" label="选手HASH值"> </el-table-column>
        </el-table>
      </div>
      <!-- 打印 -->
      <el-row>
        <el-col :offset="20"
          ><el-button @click="printTable" type="primary" class="print define"
            ><i class="iconfont icon-dayin-dayinji"> </i
            ><span class="printSize">打印</span></el-button
          ></el-col
        >
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { printExcel } from '@/utils/config'
export default {
  data () {
    return {
      // 创建比赛的参数
      userForm: {
        gamename: '',
        num: '',
        token: '',
        username: ''
      },
      // 表单验证
      userRules: {
        gamename: [
          { required: true, message: '请输入比赛名称', trigger: 'blur' }
        ],
        num: [
          { required: true, message: '比赛人数不能为空' },
          { type: '', message: '比赛人数必须为数字' }
        ],
        game_id: [
          { required: true, message: '比赛ID不能为空' },
          { type: '', message: '比赛ID必须为数字' }
        ]
      },
      // 表格内容
      HashData: [],
      // 获取最近一场比赛信息请求参数
      getGame: {
        token: '',
        username: ''
      },
      // 搜索比赛输入的id
      searchGame: {
        token: '',
        username: '',
        game_id: ''
      }

    }
  },
  mounted () {
    this.userForm.token = window.sessionStorage.getItem('token')
    this.userForm.username = window.sessionStorage.getItem('username')
    this.getGame.token = window.sessionStorage.getItem('token')
    this.getGame.username = window.sessionStorage.getItem('username')
    this.searchGame.token = window.sessionStorage.getItem('token')
    this.searchGame.username = window.sessionStorage.getItem('username')
    this.getOneGame()
  },
  methods: {
    // 1.1 创建比赛和比赛人数
    submitUserForm () {
      // 1.2 表单验证
      this.$refs.userFormRef.validate(async (valid) => {
        if (!valid) return
        // 1.3 发送请求
        const { data: res } = await this.$http.post('/foundGame', this.userForm)
        // 1.4 判断状态码
        if (res.status !== 200) {
          return this.$message.error('生成比赛失败！请检查是否已经有这场比赛')
        }
        // 1.5 请求成功 赋值渲染表格
        this.HashData = res.data.hash_list
        this.$message({
          message: '生成比赛成功！',
          type: 'success'
        })
        // 1.6 清空输入框
        this.resetUserForm('userFormRef')
      })
    },

    //  2.1 清空输入框
    resetUserForm (Ref) {
      this.$refs[Ref].resetFields()
    },
    // 3.1 请求最近一场比赛
    async getOneGame () {
    //  3.2 发请求
      const { data: res } = await this.$http.post('/lastGame', this.getGame)
      // 3.3 判断状态码
      if (res.status !== 200) {
        return
      }
      // 3.4 状态码正确 赋值
      this.HashData = res.data.hash_list
    },
    //  搜索比赛
    searchGameHash () {
      this.$refs.searchGameRef.validate(async (valid) => {
        if (!valid) return
        const { data: res } = await this.$http.post('getHash', this.searchGame)
        if (res.status !== 200) {
          return this.$message.error('搜索比赛失败！')
        }
        // 判断返回回来的数组是否为空
        if (res.data.all_hash.length === 0) {
          return this.$message.error('没有该场比赛的数据！')
        }
        this.$message({
          type: 'success',
          message: '搜索成功！'
        })
        this.HashData = res.data.all_hash
      })
    },
    // 打印
    printTable () {
      printExcel('export')
    }
  }
}
</script>

<style lang="less" scoped>
.el-form {
  margin-top: 20px;
}
.btn {
  width: 120px;
  font-size: 15px;
  text-align: center;

  color: #fff;
  letter-spacing: 2px;
}

i {
  font-size: 20px;
}
.print {
  margin-top: 30px;
  width: 150px;
  text-align: center;

  .printSize {
    font-size: 17px;
    margin-left: 3px;
  }
}

</style>
