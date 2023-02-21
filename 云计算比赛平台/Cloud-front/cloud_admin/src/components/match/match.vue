<template>
  <div>
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/users' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>比赛管理</el-breadcrumb-item>
        <el-breadcrumb-item>赛前准备</el-breadcrumb-item>
      </el-breadcrumb>
    <el-row :gutter="30">
      <el-col :span="12" v-for="(item, index) in gameDataList" :key="item.game_id">
      <el-card>
        <div class="cardInfo">
        <h1>{{item.game_name}}</h1>
        <p>比赛ID：<span>{{item.game_id}}</span></p>
        <p>比赛人数：<span>{{item.game_people}}</span>人</p>
        <p>比赛状态：<span v-show="item.game_status==0">未开始</span><span v-show="item.game_status==1">进行中</span><span v-show="item.game_status==2">暂停中</span></p>
        <p>比赛创建时间：<span>{{item.game_time}}</span></p>
        <p>题目组：<span>{{item.group_name}}</span></p>
      <div class="btnStatus">
          <el-button type="primary" class="define" @click="setGame(item.game_id)"  >选择题组</el-button>
          <el-button type="primary" class="define" @click="adminGame(index)"  >比赛管理</el-button>
          <el-button type="primary" class="ranking define" @click="rankingList(index)">排行榜</el-button>
      </div>
        </div>
      </el-card>
      </el-col>

    </el-row>
    </el-card>
    <!-- 比赛管理的抽屉 -->
    <el-drawer
  title="审核用户名"
  :visible.sync="GameDrawer"
  size='55%'
 >
 <el-table
    :data="gameUserData"
    height="85%"
    border
    style="width: 100%">
    <el-table-column
      prop="game_name"
      label="比赛名称"
  >
    </el-table-column>
     <el-table-column
      prop="hash"
      label="选手hash值">
    </el-table-column>
    <el-table-column
      prop="username"
      label="用户名"
     >
    </el-table-column>
     <el-table-column label="状态" >
      <template slot-scope="scope">
        <div class="scopeBtn">
        <el-button  type="warning" class="btnyellow" size="small" v-if="scope.row.status =='wating'||scope.row.status =='init'">待审核</el-button>
        <el-button  class="empty" size="small" v-if="scope.row.status =='noruning'">已驳回</el-button>
        <el-button class="define" size="small" v-if="scope.row.status =='runing'" >已通过</el-button>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="审核">
      <template slot-scope="scope">
        <div class="scopeBtn">
        <el-button class="define" size="small" @click="adoptUserName(scope.row)">通过</el-button>
        <el-button class="empty" size="small"  @click="rejectUserName(scope.row)">驳回</el-button>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-button  type="danger" class="btnGame empty" @click="deleteGame">删除比赛</el-button>
  <el-button  type="warning" class="btnGame btnyellow" @click="suspendGame">暂停比赛</el-button>
  <el-button  type="primary" class="btnGame define"  @click="startGame">开始比赛</el-button>
  </el-drawer>
  <!-- 排行榜的抽屉 -->
  <el-drawer
    :visible.sync="rankingListDrawer"
    size='55%'
    title="得分排行榜"
    class="rankingListDrawer"
  >
  <el-table
    :data="rankingdata"
    height="90%"
    border
    class="ranking">
    <el-table-column
      type="index"
      label="排名"
      width="80px"
      >
    <template slot-scope="scope">
      <img v-if="scope.$index == 0" src="../../assets/image/pm/one.png" alt="" />
      <img v-else-if="scope.$index == 1" src="../../assets/image/pm/two.png" alt=""/>
      <img v-else-if="scope.$index == 2" src="../../assets/image/pm/three.png" alt=""/>
      <span v-else>{{ scope.$index + 1 }}</span>
  </template>
    </el-table-column>
    <el-table-column
      prop="username"
      label="选手名称">
    </el-table-column>
    <el-table-column
      prop="accomplish"
      label="完成题目总数">
    </el-table-column>
     <el-table-column
      prop="result"
      label="总分">
    </el-table-column>
    </el-table>
  </el-drawer>
<!-- 选择题目组对话框 -->
<el-dialog
  title="提示"
  :visible.sync="topicDialogVisible"
  width="30%"
>
    <el-form
        :model="topicGroupList"
        :rules="topicGroupRules"
        ref="topicGroupRuleForm"
        label-width="100px"
      >
        <el-form-item label="选择题目组" prop="group_id">
          <el-select
            v-model="topicGroupList.group_id"
            placeholder="请选择"
          >
            <el-option
              v-for="item in topicdata"
              :key="item.id"
              :label="item.groupname"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
  <span slot="footer" class="dialog-footer">
    <el-button @click="topicDialogVisible = false">取 消</el-button>
    <el-button type="primary" class="define" @click="choiceTopic">确 定</el-button>
  </span>
</el-dialog>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // 抽屉状态
      GameDrawer: false,
      // 排行榜的抽屉
      rankingListDrawer: false,
      // 排行榜的数据
      rankingdata: [],
      // 比赛状态
      gameFlag: null,
      // 所有比赛的数据
      gameDataList: [],
      // 审核用户名数据
      gameUserData: [],
      // 选择题目组对话框
      topicDialogVisible: false,
      // 所有题目组的数据
      topicdata: [],
      // 选择题目组请求参数
      topicGroupList: {
        game_id: '',
        group_id: '',
        token: '',
        username: ''
      },
      // 表单验证
      topicGroupRules: {
        group_id: [{ required: true, message: '请选择题目组', trigger: 'blur' }]
      },
      // 获取所有比赛的请求参数
      getGame: {
        token: '',
        username: ''
      },
      // 查看比赛排行榜请求参数
      getRankingList: {
        token: '',
        username: '',
        game_id: ''
      },
      // 获取这场比赛要审核的用户
      getHash: {
        token: '',
        username: '',
        game_id: ''
      },
      // 审核用户名请求参数
      auditingName: {
        token: '',
        username: ''
      },
      // 删除比赛请求参数
      deGame: {
        token: '',
        username: '',
        gamename: ''
      },
      // 开始比赛和暂停比赛的请求参数
      staGame: {
        token: '',
        username: '',
        game_id: ''
      },
      // 比赛轮询定时器
      gameTimer: null

    }
  },
  mounted () {
    // 获取所有比赛
    this.getGame.token = window.sessionStorage.getItem('token')
    this.getGame.username = window.sessionStorage.getItem('username')
    // 选择题目组
    this.topicGroupList.token = window.sessionStorage.getItem('token')
    this.topicGroupList.username = window.sessionStorage.getItem('username')
    // 排行榜
    this.getRankingList.token = window.sessionStorage.getItem('token')
    this.getRankingList.username = window.sessionStorage.getItem('username')
    // 获取审核用户
    this.getHash.token = window.sessionStorage.getItem('token')
    this.getHash.username = window.sessionStorage.getItem('username')
    // 审核用户名
    this.auditingName.token = window.sessionStorage.getItem('token')
    this.auditingName.username = window.sessionStorage.getItem('username')
    // 删除比赛
    this.deGame.token = window.sessionStorage.getItem('token')
    this.deGame.username = window.sessionStorage.getItem('username')
    // 开始比赛和暂停比赛
    this.staGame.token = window.sessionStorage.getItem('token')
    this.staGame.username = window.sessionStorage.getItem('username')

    this.getGameList()
    this.getGameTopicGroup()
  },
  methods: {
    // 1.1 获取所有的比赛

    async getGameList () {
      // 1.2 发请求
      const { data: res } = await this.$http.post('/getallGame', this.getGame)
      // 1.3 判断状态码
      if (res.status !== 200) {
        return this.$message.error('获取所有比赛失败')
      }
      res.data.all_game.reverse()
      this.gameDataList = res.data.all_game
    },
    // 1.2 获取所有的题目组
    async getGameTopicGroup () {
      const { data: res } = await this.$http.post('/showGroup', this.getGame)
      if (res.status !== 200) {
        return this.$message.error('获取题目组列表失败')
      }
      this.topicdata = res.data.all_group
    },
    // 选择题目组对话框
    setGame (gameid) {
      this.topicGroupList.game_id = gameid
      this.topicDialogVisible = true
    },
    // 选择题目组
    async choiceTopic () {
      this.$refs.topicGroupRuleForm.validate(async (valid) => {
        if (!valid) return
        const { data: res } = await this.$http.post('setGameid', this.topicGroupList)
        if (res.status !== 200) {
          return this.$message.error('选择题目组失败')
        }
        this.getGameList()
        this.topicDialogVisible = false
        this.topicGroupList.group_id = ''
        this.$message({
          type: 'success',
          message: '选择题目组成功'
        })
      })
    },
    // 点击比赛管理
    adminGame (index) {
      // 赋值 删除比赛的比赛名称
      this.deGame.gamename = this.gameDataList[index].game_name
      // 赋值 开始比赛的id
      this.staGame.game_id = this.gameDataList[index].game_id
      // 赋值 比赛是否进行中的状态
      this.gameFlag = this.gameDataList[index].game_status
      // 审核用户名
      this.getHash.game_id = this.gameDataList[index].game_id
      this.gameTimer = setInterval(async () => {
        const { data: res } = await this.$http.post('getHash', this.getHash)
        if (res.status !== 200) return
        this.gameUserData = res.data.all_hash
      }, 500)
      this.GameDrawer = true
    },

    // 通过用户名
    async adoptUserName (scope) {
      this.auditingName.id = scope.id
      const { data: res } = await this.$http.post('success', this.auditingName)
      if (res.status !== 201) return
      this.$message({
        message: `已同意${scope.username}选手使用该用户名`,
        type: 'success'
      })
    },
    // 驳回用户名
    async  rejectUserName (scope) {
      this.auditingName.id = scope.id
      const { data: res } = await this.$http.post('refuse', this.auditingName)
      if (res.status !== 404) return
      this.$message({
        message: `已同意${scope.username}选手使用该用户名`,
        type: 'success'
      })
      this.$message({
        message: `已驳回${scope.username}选手使用该用户名`,
        type: 'success'
      })
    },
    // 查看比赛排行榜
    rankingList (index) {
      this.rankingListDrawer = true
      this.getRankingList.game_id = this.gameDataList[index].game_id
      this.gameTimer = setInterval(async () => {
        // 请求参数
        const { data: res } = await this.$http.post('/rankingList', this.getRankingList)
        if (res.status !== 200) {
          return this.$message.error('获取排行榜数据失败')
        }
        // 排序
        this.rankingdata = res.data.all_score.sort((a, b) => {
          return b.result - a.result
        })
      }, 500)
    },
    // 删除比赛
    async  deleteGame () {
      // 判断比赛是否进行中 进行中不能删除比赛
      console.log(this.gameFlag)
      if (this.gameFlag === 1) {
        return this.$message.error('比赛正在进行中，删除比赛失败！')
      }
      this.$confirm('是否删除该比赛?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const { data: res } = await this.$http.post('deleteGame', this.deGame)
        if (res.status !== 200) {
          return this.$message.error('删除比赛失败！')
        }
        this.$message({
          type: 'success',
          message: '删除比赛成功！'
        })
        this.GameDrawer = false
        this.getGameList()
      })
    },
    // 开始比赛
    startGame () {
      this.$confirm('是否正式开始比赛?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const { data: res } = await this.$http.post('startGame', this.staGame)
        if (res.status !== 200) {
          return this.$message.error('开始比赛失败！')
        }
        this.$message({
          type: 'success',
          message: '开始比赛成功！请提醒选手开始比赛！'
        })
        this.GameDrawer = false
        this.getGameList()
      })
    },
    // 暂停比赛
    async  suspendGame () {
      this.$confirm('是否暂停比赛?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const { data: res } = await this.$http.post('stopGame', this.staGame)
        if (res.status !== 200) {
          return this.$message.error('暂停比赛失败！')
        }
        this.$message({
          type: 'success',
          message: '暂停比赛成功！'
        })
        this.GameDrawer = false
        this.getGameList()
      })
    }

  },
  watch: {
    GameDrawer: function (newVal, oldVal) {
      // 比赛管理抽屉关闭时，清空定时器
      if (newVal === false) {
        clearInterval(this.gameTimer)
      }
    },
    rankingListDrawer: function (newVal, oldVal) {
      // 排行榜抽屉关闭时，清空定时器
      if (newVal === false) {
        clearInterval(this.gameTimer)
      }
    }

  }

}
</script>
<style lang="less" scoped>
  .el-row{
    margin-top: 30px;

    .el-card{
      margin-bottom: 30px;

  }
  .cardInfo{
    color: #fff;
    font-weight: bold;
    display: flex;
    flex-direction: column;

  h1{
      color: rgb(242,203,108);
      align-self: center;
  }
  p{
    font-size: 14px;
    padding-top: 10px;
    line-height: 1.5em;
    span{
      padding:0px 5px;
      color: rgb(242,203,108);
      font-weight: bold;
    }
  }
  .btnStatus{
    margin: 30px 0 10px;
    align-self: flex-end;
    .el-button{
      font-weight: bold;
      letter-spacing: 3px;
    }
  }
}
}
.btnGame{
  float: right;
  display: block;
  margin: 10px;
}
.ranking{
  margin: 10px;
}
img{
  width: 40px;
  height: 40px;
}
.btnyellow{
  font-weight: bold;
  border: none;
  color: #fff;
  background-color: rgb(242,203,108);
}
</style>
