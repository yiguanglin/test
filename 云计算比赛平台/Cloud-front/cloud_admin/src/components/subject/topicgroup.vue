<template>
  <div class="container">
    <el-card>
      <!-- 面包屑 -->
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/users' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>题目管理</el-breadcrumb-item>
        <el-breadcrumb-item>题目组</el-breadcrumb-item>
      </el-breadcrumb>
      <!-- 添加题目按钮 -->
      <el-button class="define" @click="topicDialogVisible = true">新建题目组</el-button>
      <el-button class="define" @click="topicListDrawer = true">题目列表</el-button>
      <el-divider content-position="left">题目组列表</el-divider>
      <!-- 展示题目组列表 -->
      <div class="topicGroup">
        <el-card v-for="(item,index) in getTopicGroup" :key="item.id">
          <h1>{{item.groupname}}</h1>
          <p>题数:<span>{{item.sum}}</span>题</p>
          <el-button class="define" @click="topicAdministration(index)"
            >题目组管理</el-button
          >
        </el-card>
      </div>
    </el-card>
    <!-- 新建题目组对话框 -->
    <el-dialog
      title="新建题目组"
      :visible.sync="topicDialogVisible"
      width="30%"
    >
      <el-form
        :model="topicGroupList"
        :rules="topicGroupRules"
        ref="topicGroupListRuleForm"
        label-width="100px"

      >

        <el-form-item label="题目组名称" prop="groupname">
          <el-input v-model="topicGroupList.groupname"></el-input>
        </el-form-item>
        <el-form-item label="选择题目" prop="subject_list">
          <el-select
            v-model="topicGroupList.subject_list"
            multiple
            placeholder="请选择"
          >
            <el-option
              v-for="item in topicdata"
              :key="item.id"
              :label="item.headline"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="topicDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="newTopicGroup" class="define"
          >确 定</el-button
        >
      </span>
    </el-dialog>
    <!-- 题目组管理抽屉 -->
    <el-drawer title="题目组管理" :visible.sync="topicGroupDrawer" size="50%">
      <h1>题目列表</h1>
      <el-table
        :data="oneTopicGroupData"
        height="450"
        border
      >
        <el-table-column
          type="index"
          label="#">
        </el-table-column>
        <el-table-column
          prop="headline"
          label="题目名称">
        </el-table-column>
         <el-table-column
      prop="level"
      label="难度等级">
    </el-table-column>
        <el-table-column
      prop="answer"
      label="题目答案">
    </el-table-column>
        <el-table-column
          label="操作">
          <template slot-scope="scope">
            <el-button class="empty" @click="deleteGroupSubject(scope.row)">移除</el-button>
          </template>
        </el-table-column>
        </el-table>
          <el-button class="define btn" @click="topicGroupDrawer = false">关闭</el-button>
          <el-button class="define btn" @click="addTopicDialogVisible = true">新增题目</el-button>
          <el-button class="empty btn" @click="deleteTopicGroup">删除题目组</el-button>
    </el-drawer>
    <!-- 所有题目列表的抽屉 -->
  <el-drawer
    :visible.sync="topicListDrawer"
    size='55%'
    title="题目列表"

  >
  <el-table
    :data="topicdata"
    height="450"
    border
    class="ranking">
    <el-table-column
      type="index"
      label="#">
    </el-table-column>
    <el-table-column
      prop="headline"
      label="题目名称">
    </el-table-column>
     <el-table-column
      prop="level"
      label="难度等级">
    </el-table-column>
     <el-table-column
      prop="answer"
      label="题目答案">
    </el-table-column>
     <el-table-column
      label="操作">
      <template slot-scope="scope">
        <el-button class="define" @click="modifyTopic(scope.row)">编辑</el-button>
        <el-button class="empty" @click="deleteTopic(scope.row)">删除</el-button>
      </template>
    </el-table-column>
    </el-table>
  </el-drawer>
  <!-- 编辑题目抽屉 -->
 <el-drawer title="编辑题目" :visible.sync="TextDialogVisible" size="50%">
    <el-form :model="upload" :rules="uploadRules" ref="uploadRef" label-width="100px"  width="60%">
  <el-form-item label="题目名称:" prop="headline">
    <el-input v-model="upload.headline"></el-input>
  </el-form-item>
    <el-form-item label="题目内容:" prop="text">
    <el-button class="define" @click="TextDialogVisibleEdit = true">
      点我输入
    </el-button>
  </el-form-item>
  <el-form-item label="题目答案:" prop="answer">
    <el-input v-model="upload.answer"></el-input>
  </el-form-item>
   <el-form-item label="题目分数:" prop='grade'>
    <el-input v-model.number="upload.grade" autocomplete="off"></el-input>
  </el-form-item>
  <el-form-item label="难度等级:" prop="level">
    <el-select v-model="upload.level" placeholder="请选择">
    <el-option
      v-for="item in levelOptions"
      :key="item.value"
      :label="item.label"
      :value="item.value">
    </el-option>
  </el-select>
  </el-form-item>
   <el-form-item >
    <el-button class="define" @click="uploadSubject">
      完成编辑
    </el-button>
  </el-form-item>
     </el-form>
<!-- 编辑题目内容弹框 -->
 </el-drawer>
 <!-- 编辑题目内容对话框 -->
 <el-dialog
  title="编辑题目内容"
  :visible.sync="TextDialogVisibleEdit"
  width="80%"
  >
     <mavon-editor v-model="upload.text" :toolbars="toolbars" />
  <span slot="footer" class="dialog-footer">
    <el-button @click="TextDialogVisibleEdit = false">取 消</el-button>
    <el-button class="define" @click=" TextDialogVisibleEdit = false">确 定</el-button>
  </span>
</el-dialog>
<!-- 新增题目对话框 -->
 <el-dialog
  title="请选择题目"
  :visible.sync="addTopicDialogVisible"
        width="30%"
  >
      <el-form
        :model="topicList"
        :rules="topicGroupRules"
        ref="addTopicRuleForm"
      >
        <el-form-item label="选择题目" prop="subject_list">
          <el-select
            v-model="topicList.subject_list"
            multiple
            placeholder="请选择"
          >
            <el-option
              v-for="item in  topicdata"
              :key="item.id"
              :label="item.headline"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addTopicDialogVisible = false">取 消</el-button>
    <el-button class="define" @click="addTopicList">确 定</el-button>
      </span>

</el-dialog>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // 新建题目组对话框
      topicDialogVisible: false,
      // 新建题目组请求参数
      topicGroupList: {
        groupname: '',
        subject_list: [],
        token: '',
        username: ''

      },
      // 题目组表单验证
      topicGroupRules: {
        game_id: [{ required: true, message: '请输入比赛ID', trigger: 'blur' }],
        groupname: [{ required: true, message: '请输入题目组名称', trigger: 'blur' }],
        subject_list: [{ required: true, message: '请选择题目', trigger: 'blur' }]
      },

      // 题目组管理抽屉
      topicGroupDrawer: false,
      // 所有题目列表抽屉
      topicListDrawer: false,
      // 所有题目的列表
      getTopicGroup: [],
      // 选择所有题目组的数据
      topicdata: [],
      // 获取所有题目列表参数
      topicParameter: {
        username: '',
        token: ''
      },
      // 单个题目组里的题目请求数据
      onegroup: {
        token: '',
        username: '',
        group_id: ''
      },
      // 移除题目组的题目请求参数
      removeTopic: {
        token: '',
        username: '',
        group_id: '',
        all_subject: ''
      },
      // 删除题目组参数
      deTopicGroup: {
        token: '',
        username: '',
        id: ''
      },
      // 题目组添加题目对话框
      addTopicDialogVisible: false,
      // 题目组添加题目参数
      topicList: {
        token: '',
        username: '',
        subject_list: [],
        group_id: ''
      },
      // 单个题目组的数据
      oneTopicGroupData: [],
      // 编辑题目的相关配置
      // 编辑题目对话框
      TextDialogVisible: false,
      // 编辑内容弹框
      TextDialogVisibleEdit: false,
      upload: {
        headline: '',
        text: '',
        answer: '',
        grade: '',
        level: '',
        url: '',
        token: '',
        username: ''
      },
      // 表单验证
      uploadRules: {
        headline: [{ required: true, message: '题目名称不能为空', trigger: 'blur' }],
        text: [{ required: true, message: '题目内容不能为空', trigger: 'blur' }],
        answer: [{ required: true, message: '题目答案不能为空', trigger: 'blur' }],
        grade: [
          { required: true, message: '题目分数不能为空' },
          { type: 'number', message: '题目分数必须为数字' }
        ],
        level: [{ required: true, message: '题目难度不能为空', trigger: 'blur' }]
      },
      // 题目难度
      levelOptions: [
        {
          value: '1',
          label: '简单'
        },
        {
          value: '2',
          label: '容易'
        }, {
          value: '3',
          label: '中等'
        }, {
          value: '4',
          label: '困难'
        }, {
          value: '5',
          label: '非常困难'
        }
      ],
      // markdown 相关配置
      toolbars: {
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        mark: true, // 标记
        superscript: true, // 上角标
        quote: true, // 引用
        ol: true, // 有序列表
        link: true, // 链接
        imagelink: true, // 图片链接
        help: true, // 帮助
        code: true, // code
        subfield: true, // 是否需要分栏
        fullscreen: true, // 全屏编辑
        readmodel: true, // 沉浸式阅读
        undo: true, // 上一步
        trash: true, // 清空
        save: true, // 保存（触发events中的save事件）
        navigation: true // 导航目录
      }

    }
  },
  mounted () {
    // 获取所有题目列表参数
    this.topicParameter.username = window.sessionStorage.getItem('username')
    this.topicParameter.token = window.sessionStorage.getItem('token')
    // 新建题目组请求参数
    this.topicGroupList.username = window.sessionStorage.getItem('username')
    this.topicGroupList.token = window.sessionStorage.getItem('token')
    // 单个题目组里的题目请求数据
    this.onegroup.token = window.sessionStorage.getItem('token')
    this.onegroup.username = window.sessionStorage.getItem('username')
    // 移除题目组的题目请求参数
    this.removeTopic.token = window.sessionStorage.getItem('token')
    this.removeTopic.username = window.sessionStorage.getItem('username')
    // 删除题目组参数
    this.deTopicGroup.username = window.sessionStorage.getItem('username')
    this.deTopicGroup.token = window.sessionStorage.getItem('token')
    // 题目组添加题目参数
    this.topicList.token = window.sessionStorage.getItem('token')
    this.topicList.username = window.sessionStorage.getItem('username')
    this.getTopicList()
    this.showGroup()
  },
  methods: {
    // 获取所有的题目
    async  getTopicList () {
      const { data: res } = await this.$http.post('/allSubject', this.topicParameter)
      this.topicdata = res.data.all_subject.reverse()
    },
    // 获取所有题目组
    async showGroup () {
      const { data: res } = await this.$http.post('/showGroup', this.topicParameter)
      if (res.status !== 200) {
        return this.$message.error('获取题目组列表失败')
      }
      this.getTopicGroup = res.data.all_group.reverse()
    },
    // 新建题目组
    newTopicGroup () {
      this.$refs.topicGroupListRuleForm.validate(async (valid) => {
        if (!valid) return
        this.topicDialogVisible = false
        const { data: res } = await this.$http.post('/foundGroup', this.topicGroupList)
        this.$refs.topicGroupListRuleForm.resetFields()
        if (res.status !== 200) {
          return this.$message.error('新建题目组失败')
        }
        this.$message({
          message: '新建题目组成功',
          type: 'success'
        })
        this.showGroup()
      })
    },
    // 题目组管理
    topicAdministration (index) {
      // 获取单个题目组里的题目id
      this.onegroup.group_id = this.getTopicGroup[index].id
      this.getOneTopicGroupData()
      // 移除题目组题目id
      this.removeTopic.group_id = this.getTopicGroup[index].id
      // 删除题目的id
      this.deTopicGroup.id = this.getTopicGroup[index].id
      // 往题目组里面添加题目的id
      this.topicList.group_id = this.getTopicGroup[index].id
      // 打开弹框
      this.topicGroupDrawer = true
    },
    // 获取单个题目组里的题目
    async getOneTopicGroupData () {
      const { data: res } = await this.$http.post('onegroup', this.onegroup)
      if (res.status !== 200) {
        return this.$message.error('获取该题目组的题目失败')
      }
      this.oneTopicGroupData = res.data.subject_list
    },
    // 移除题目组里的题目
    deleteGroupSubject (scope) {
      this.$confirm('确认要移除该题目吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        this.removeTopic.all_subject = scope.subject_id
        const { data: res } = await this.$http.post('deleteGroupSubject', this.removeTopic)
        if (res.status !== 200) {
          return this.$message.error('移除题目失败')
        }
        this.getOneTopicGroupData()
        this.showGroup()
        this.$message({
          type: 'success',
          message: '移除成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消移除'
        })
      })
    },
    // 编辑题目
    modifyTopic (scope) {
      this.upload = scope
      this.TextDialogVisible = true
    },
    // 删除题目
    async deleteTopic (scope) {
      this.$confirm('确定要删除该题目吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        var deleteTopicParameter = this.topicParameter
        deleteTopicParameter.subject_id = scope.id
        const { data: res } = await this.$http.post('deleteSubject', deleteTopicParameter)
        if (res.status !== 200) {
          return this.$message.error('删除题目失败')
        }
        this.showGroup()
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
        this.getTopicList()
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },

    // 确认编辑

    async  uploadSubject () {
      var htmlContent = this.converter.makeHtml(this.upload.text)
      this.upload.text = htmlContent
      this.upload.username = window.sessionStorage.getItem('username')
      this.upload.token = window.sessionStorage.getItem('token')
      const { data: res } = await this.$http.post('updateSubject', this.upload)
      this.TextDialogVisible = false
      if (res.status !== 200) {
        return this.$message.error('编辑失败')
      }
      this.$message({
        message: '编辑成功',
        type: 'success'
      })
    },
    // 删除题目组
    async deleteTopicGroup () {
      this.$confirm('确认要删除该题目组吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const { data: res } = await this.$http.post('deleteGroup', this.deTopicGroup)
        if (res.status !== 200) {
          return this.$message.error('删除题目组失败')
        }
        this.topicGroupDrawer = false
        this.$message({
          type: 'success',
          message: '删除题目组成功!'
        })
        this.showGroup()
      })
    },
    // 往题目组里面添加题目
    addTopicList () {
      this.$refs.addTopicRuleForm.validate(async (valid) => {
        if (!valid) return
        this.addTopicDialogVisible = false
        const { data: res } = await this.$http.post('addsubject', this.topicList)
        if (res.status !== 200) {
          return this.$message.error('新增题目失败')
        }
        this.topicList.subject_list = []
        this.$message({
          message: '新增题目成功',
          type: 'success'
        })
        this.getOneTopicGroupData()
        this.showGroup()
      })
    }
  }
}
</script>

<style lang="less" scoped>
.container{
  height: auto;
}
.el-breadcrumb {
  margin-bottom: 25px;
}
.topicGroup {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
    &::after{
      content: '';
      display: block;
      width: 30%;
  }
  .el-card {
    margin: 0 0 30px;
    display:inline-block;
    color: #fff;
    width: 30%;

    h1 {
      color: rgb(242,203,108);
      text-align: center;
      padding: 7px 0;
    }
    p {
      line-height: 1.5em;
      span{
      color: rgb(242,203,108);
      font-weight: bold;
      padding: 0 3px;
  }
    }
    .el-button {
      margin: 10px 0;
      float: right;
    }
  }
}
h1{
  color: #fff;
  padding: 10px 0;
}
.btn{
  margin: 30px 10px;
float: right;
}
</style>
