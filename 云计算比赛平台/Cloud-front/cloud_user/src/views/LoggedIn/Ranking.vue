<template>
  <div class="ranking">
    <!-- 排行榜 -->
    <h1>云计算挑战平台</h1>

    <!-- 轮播图 -->
    <div class="rotationmap">
      <!-- 左 -->
      <div class="left" @click="marker"></div>

      <!-- 内容 -->
      <div class="map">
        <div class="cont" ref="mapRef">
          <div class="rk">
            <h1>积分排行榜</h1>
            <el-table
              class="table"
              :data="RankingListData"
              height="500px"
              style="width: 100%"
            >
              <!-- 排名 -->
              <el-table-column
                prop="date"
                label="排名"
                type="index"
                width="100px"
              >
                <template slot-scope="s">
                  <!-- {{s.$index}} -->
                  <img v-if="s.$index == 0" src="~@/img/排名/one.png" alt="" />
                  <img
                    v-else-if="s.$index == 1"
                    src="~@/img/排名/two.png"
                    alt=""
                  />
                  <img
                    v-else-if="s.$index == 2"
                    src="~@/img/排名/three.png"
                    alt=""
                  />
                  <span v-else>{{ s.$index + 1 }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="username" label="用户名">
              </el-table-column>
              <el-table-column prop="accomplish" label="完成题目数">
              </el-table-column>
              <el-table-column prop="result" label="得分"> </el-table-column>
            </el-table>
          </div>

          <div class="score">
            <h1>我的得分事件</h1>
            <el-table
              class="table"
              :data="getUserFractionList"
              height="500px"
              style="width: 100%"
            >
              <el-table-column prop="headline" label="题目名称">
              </el-table-column>
              <el-table-column prop="grade" label="加分"> </el-table-column>
              <el-table-column prop="time" label="时间"> </el-table-column>
            </el-table>
          </div>

          <div class="se">
            <h1>得分事件预览</h1>
            <div class="news">
              <el-table
                class="table"
                :data="ScoringEvent"
                height="500px"
                style="width: 100%"
              >
                <el-table-column prop="username" label="用户名">
                </el-table-column>
                <el-table-column prop="headline" label="题目标题">
                </el-table-column>
                <el-table-column prop="grade" label="分数"> </el-table-column>
                <el-table-column prop="time" label="完成时间">
                </el-table-column>
              </el-table>
            </div>
          </div>

          <div class="os">
            <h1>全局比赛详情</h1>
            <el-table
              class="table"
              :data="tableData"
              height="500px"
              style="width: 100%"
            >
              <el-table-column prop="date" label="题目名称"> </el-table-column>
              <el-table-column prop="name" label="成功次数"> </el-table-column>
              <el-table-column prop="address" label="失败次数">
              </el-table-column>
              <el-table-column prop="address" label="挑战成功率">
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>

      <!-- 右 -->
      <div class="right" @click="markers"></div>
    </div>

    <!-- 下面的指示器 -->
    <div class="indicator">
      <div class="d1">
        <span @click="stopit = !stopit" v-show="stopit"
          >自动轮播中<i class="iconfont icon-kaishi"></i
        ></span>
        <span @click="stopit = !stopit" v-show="!stopit"
          >暂停中<i class="iconfont icon-zanting"></i
        ></span>
      </div>
      <div class="d2">
        <div
          v-for="(i, index) in 3"
          :key="(i, index)"
          :style="index == rotation ? 'background: #a8ff78;' : ''"
          @click="indicatorFun(index)"
        ></div>
      </div>
    </div>

    <!-- 呼吸灯。。。 -->
    <decorate />

    <!-- 返回 -->
    <div class="botton">
      <div @click="returnFun"><i class="iconfont icon-fanhui"></i></div>
    </div>
  </div>
</template>

<script>
import decorate from "@/components/decorate";
export default {
  components: {
    decorate,
  },
  data() {
    return {
      // 积分排行榜
      RankingListData: [],
      // 我的得分事件
      getUserFractionList: [],
      // 得分事件
      ScoringEvent: [],

      tableData: [],
      // 请求所需参数
      parameter: {
        hashcode: "",
        token: "",
      },
      gameId: "",//比赛id
      // 用户id
      usernameId: "",
      // 当前轮播所在位置，可手动设置0-2
      rotation: 0,
      stopit: true, // 设置停止
      stop: true,
      // map:0,
      // 定时请求
      mapfSet: null,
      globaltiming: null,
    };
  },
  created() {
    // 获取初始值
    this.parameter.hashcode = sessionStorage.getItem("hashcode");
    this.parameter.token = sessionStorage.getItem("token");
    this.usernameId = sessionStorage.getItem("id");
    this.gameId = sessionStorage.getItem("game_id");

    this.RankingListFn();
    this.ScoringEventFn();
    this.getUserFractionFn();
  },
  methods: {
    // 获取用户得分事件
    async getUserFractionFn() {
      let obj = {
        ...this.parameter,
        user_id: this.usernameId,
      };
      let { data } = await this.$http.post("/userThing", obj);
      this.getUserFractionList = data.data.subject_list;
    },
    // 获取得分事件
    async ScoringEventFn() {
      let obj = {
        ...this.parameter,
        game_id: this.gameId,
      };
      let { data } = await this.$http.post("/event", obj);
      this.ScoringEvent = data.data.all_event;
    },
    // 获取积分排行榜
    async RankingListFn() {
      let obj = {
        ...this.parameter,
        game_id: this.gameId,
      };
      let { data } = await this.$http.post("/rankingList", obj);
      this.RankingListData = data.data.all_score;
    },
    // 轮播
    mapf() {
      this.$refs.mapRef.style.left = `-${this.rotation * 100}%`;
      this.mapfSet = setInterval(() => {
        if (this.rotation == 2) {
          this.rotation = 0;
          this.$refs.mapRef.style.left = `-${this.rotation * 100}%`;
        } else {
          this.rotation += 1;
          this.$refs.mapRef.style.left = `-${this.rotation * 100}%`;
        }
      }, 5000);
    },
    // 定时请求获取得分事件、积分排行榜
    getGlobalData() {
      this.globaltiming = setInterval(() => {
        this.ScoringEventFn();
        this.RankingListFn();
      }, 2000);
    },

    // 点击下面小按钮
    indicatorFun(i) {
      this.rotation = i;
      this.$refs.mapRef.style.left = `-${i * 100}%`;
    },
    // 左指示器
    marker() {
      if (this.rotation <= 0) {
        this.rotation = 2;
        return;
      }
      this.rotation--;
      this.antishake();
    },
    // 右指示器
    markers() {
      if (this.rotation >= 2) {
        this.rotation = 0;
        return;
      }
      this.rotation++;
      this.antishake();
    },
    // 防抖
    antishake() {
      // this.stopit = false
      this.stop = false;
      setTimeout(() => {
        this.stop = true;
        // this.stopit = true
      }, 1000);
    },

    // 返回
    returnFun() {
      this.stopit = false;
      clearInterval(this.mapfSet);
      clearInterval(this.globaltiming);
      this.$router.push("/loggedin");
    },
  },
  mounted() {
    this.mapf();
    this.getGlobalData();
  },
  watch: {
    rotation(a, b) {
      this.$refs.mapRef.style.left = `-${a * 100}%`;
    },
    stopit(newVal, oldVal) {
      if (newVal) {
        this.mapf();
      } else {
        clearInterval(this.mapfSet);
      }
    },
  },
};
</script>

<style scoped lang="less">
@import url("~@/css/public.less");

.ranking {
  background: url("~@/img/interact.png") no-repeat center 0px;
  background-size: cover;
  background-attachment: fixed;
  width: 100%;
  // min-width: 1400px;
  min-height: 100vh;
  // border: 1px solid red;
  // display: flex;
  // justify-content: center;
  // align-items: center;
  > h1 {
    text-align: center;
    color: #fff;
    margin: 0;
    // margin-top: 10px;
    padding-top: 10px;
    margin-bottom: 34px;
  }

  .rotationmap {
    display: flex;
    justify-content: center;
    .left,
    .right {
      width: 250px;
      height: 500px;
      // border: 2px solid red;
      // flex: 1;
      color: #fff;
    }
    .left {
      background: url("~@/img/indicatorX.png") no-repeat center/auto 70%;
    }
    .right {
      background: url("~@/img/indicatorY.png") no-repeat center/auto 70%;
    }

    .map {
      flex: 1;
      min-width: 500px;
      height: auto;
      // border: 3px solid red;
      // background: #fff;
      // position: absolute;
      // left: 0;
      // right: 0;
      // margin: auto;
      color: #fff;
      overflow: hidden;
      .cont {
        width: 400%;
        height: 500px;
        // background: #fff;
        display: flex;

        position: relative;
        left: 0%;

        transition: left 0.5s;

        .rk {
          width: 100%;
          h1 {
            text-align: center;
          }
        }
        .rk,
        .score,
        .se,
        .os {
          // display: inline-block;
          width: 100%;
          // height: 300px;
          height: 450px;
          overflow: hidden;
          // border: 3px solid red;
          // background: #0ff;
          h1 {
            text-align: center;
          }
        }
        // .se {
        //   .news {
        //     width: 100%;
        //     margin: auto;
        //   }
        // }
      }
    }
  }

  .indicator {
    width: 300px;
    height: 80px;
    // background: #fff;
    margin: auto;
    padding-top: 20px;
    .d1 {
      // border: 1px solid red;
      height: 30px;
      text-align: center;
      span {
        cursor: pointer;
        color: #fff;
      }
    }
    div.d2 {
      display: flex;
      justify-content: space-evenly;
      align-items: center;
      div {
        // border: 1px solid #000;
        width: 50px;
        height: 8px;
        border-radius: 10px;
        background: rgba(204, 204, 204, 0.477);
        cursor: pointer;
      }
    }
  }
}

.table::v-deep {
  background: transparent;
  width: 100% !important;
  .el-table__body-wrapper {
    height: 300px !important;
    overflow-y: auto;
  }
  tr,
  td,
  th {
    background: transparent !important;
    color: #fff;
    text-align: center;
  }
  tr:nth-child(2n) {
    background: #203a434b !important;
  }
  tr:hover {
    background: rgba(204, 204, 204, 0.5) !important;
  }
  thead > tr {
    font-size: 20px;
    &:hover {
      background: transparent !important;
    }
  }

  > div {
    &::-webkit-scrollbar {
      width: 5px;
      background: transparent;
    }
    &::-webkit-scrollbar-thumb {
      background: rgba(204, 204, 204, 0.245);
      border-radius: 10px;
      width: 5px;
    }
  }

  img {
    width: 30px;
  }
}

.botton {
  width: 50px;

  position: fixed;
  right: 30px;
  bottom: 10px;
  margin: auto;

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

      color: #fff;
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
</style>