<template>
  <div>
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/users' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>题目管理</el-breadcrumb-item>
        <el-breadcrumb-item>上传题目</el-breadcrumb-item>
      </el-breadcrumb>

  <el-card class="card">
     <el-form :model="upload" :rules="uploadRules" ref="uploadRef" label-width="100px"  width="60%">
  <el-form-item label="题目名称:" prop="headline">
    <el-input v-model="upload.headline" placeholder="请输入题目名称"></el-input>
  </el-form-item>
    <el-form-item label="题目内容:" prop="text">
    <el-button class="define" @click="TextDialogVisible = true">
      点我输入
    </el-button>
  </el-form-item>
  <el-form-item label="题目答案:" prop="answer">
    <el-input v-model="upload.answer" placeholder="请输入题目答案"></el-input>
  </el-form-item>
   <el-form-item label="题目分数:" prop='grade'>
    <el-input v-model.number="upload.grade" autocomplete="off" placeholder="请输入题目分数"></el-input>
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
  <el-button class="empty" @click="empty">
     清空内容
    </el-button>
    <el-button class="define" @click="uploadSubject">
      上传
    </el-button>
  </el-form-item>
     </el-form>
  </el-card>
  <!--弹出md输入框 -->
<el-dialog
  title="上传题目内容"
  :visible.sync="TextDialogVisible"
  width="80%"
  >
     <mavon-editor v-model="upload.text" :toolbars="toolbars" />
  <span slot="footer" class="dialog-footer">
    <el-button @click="TextDialogVisible = false">取 消</el-button>
    <el-button class="define" @click="changeHtml">确 定</el-button>
  </span>
</el-dialog>

    </el-card>
  </div>
</template>

<script>
export default {

  data () {
    return {
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
      // 对话框
      TextDialogVisible: false,
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
      ]
    }
  },
  mounted () {
    this.upload.token = window.sessionStorage.getItem('token')
    this.upload.username = window.sessionStorage.getItem('username')
  },
  methods: {
    changeHtml () {
      this.TextDialogVisible = false
      var htmlContent = this.converter.makeHtml(this.upload.text)
      this.upload.text = htmlContent
      // 正则验证 a标签在新的页面跳转
      this.upload.text = this.upload.text.replace(/<a/gi, '<a target="_blank"')
    },
    // 上传题目
    uploadSubject () {
      this.$refs.uploadRef.validate(async (valid) => {
        if (!valid) return
        // 发请求
        const { data: res } = await this.$http.post('/upload', this.upload)
        if (res.status !== 200) {
          return this.$message({
            message: '上传失败',
            type: 'error'
          })
        }
        this.$message({
          message: '题目上传成功！',
          type: 'success'
        })
        this.empty()
      })
    },
    empty () {
      this.$refs.uploadRef.resetFields()
    }
  }
}
</script>

<style lang="less" scoped>
.card{
    margin-top: 30px;
.el-form{
  width: 50%;
}
.el-dialog{
  height: 100%;
}
}

</style>
