<template>
  <div class="container">
    <el-container>
      <!-- 头部 -->
      <el-header>
        <h1>云计算实训平台管理员系统</h1>
        <el-button @click="signOut" class="out">退出登录</el-button>
      </el-header>
      <el-container>
        <el-aside :width="iscollapse ? '64px' : '170px'">
          <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            background-color="rgb(59,117,95)"
            text-color="#fff"
            active-text-color="#2ebf91"
            router
            :collapse="iscollapse"
            :collapse-transition="false"
            unique-opened
          >
            <div class="collapse" @click="toggleCollapse">|||</div>

            <!-- 一级菜单 -->
            <el-submenu
              v-for="item in menuList"
              :key="item.id"
              :index="'/' + item.path"
            >
              <template slot="title">
                <i :class="menuIcon[item.id]"></i>
                <span>{{ item.authName }}</span>
              </template>
              <el-menu-item
                v-for="itemTow in item.chlidren"
                :key="itemTow.id"
                :index="'/' + itemTow.path"
              >
                <template slot="title">
                  <i class="iconfont icon-bisaiguanli-"></i>
                  <span>{{ itemTow.authName }}</span>
                </template>
              </el-menu-item>
            </el-submenu>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // 侧边栏数据
      menuList: [
        {
          authName: '用户管理',
          id: 1124,
          path: 'users',
          chlidren: [
            { authName: '生成HASH', id: 1125, path: 'users' }
          ]
        },
        {
          authName: '比赛管理',
          id: 1127,
          path: 'match',
          chlidren: [
            {
              authName: '赛前准备',
              id: 1128,
              path: 'match'
            }
          ]
        },
        {
          authName: '题目管理',
          id: 1131,
          path: 'subject',
          chlidren: [{ authName: '上传题目', id: 1132, path: 'subject' },
            { authName: '题目组', id: 1135, path: 'topicgroup' }]
        }
      ],
      // 侧边栏图标
      menuIcon: {
        1124: 'iconfont icon-yonghuguanli',
        1127: 'iconfont icon-bisaiguanli',
        1131: 'iconfont icon-timuguanli',
        1133: 'iconfont icon-jifenguanli'
      },
      iscollapse: false
    }
  },
  methods: {
    // 退出登录
    // 清除token
    // 跳转到login页面
    signOut () {
      // 提示是否要退出
      this.$confirm('是否退出管理员系统?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.$message({
            type: 'success',
            message: '退出成功!'
          })
          // 清除token和用户名
          window.sessionStorage.removeItem('token')
          window.sessionStorage.removeItem('username')
          // 返回到login页面
          this.$router.push('/login')
        })
        .catch(() => {})
    },
    toggleCollapse () {
      this.iscollapse = !this.iscollapse
    }
  }
}
</script>

<style lang="less" scoped>
.container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  background-color: rgb(59,117,95);
  .el-container {
    width: 100%;
    height: 100%;

    display: flex;
  }
  // 头部
  .el-header {
    color: #fff;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    h1 {
      text-shadow: 0 0 10px rgb(188, 192, 151), 0 0 20px rgb(188, 192, 151),
        0 0 30px rgb(188, 192, 151), 0 0 40px rgb(188, 192, 151);
    }
    .el-button {
      margin-right: 50px;
    }
  }
  // 侧边
  .el-aside {
    overflow: hidden;
    height: 100%;
    .el-menu {
      height: 100%;
      border: none;
      .iconfont {
        margin-right: 10px;
      }
      .el-submenu {
        font-weight: bold;
      }
    }
  }
}
.collapse {
  height: 35px;
  line-height: 35px;
  color: #fff;
  font-size: 16px;
  text-align: center;
  letter-spacing: 0.2em;
  cursor: pointer;
}
.out{
  background: rgb(167,187,195);
  color: #fff;
}
</style>
