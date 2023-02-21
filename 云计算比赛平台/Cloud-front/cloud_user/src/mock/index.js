import mockjs, { Random } from 'mockjs'
const Mock = mockjs

// 积分排行榜
Mock.mock('/rankingList', 'post', {
  "array|20": [{
    id: "@id",
    "user_id|+1": 1,
    username: "@cname",
    "result|1-100": 1,//总分
    accomplish: "@integer(1,100)"//完成的题目总数

  }]
})

// 题目
Mock.mock('/userSubject', 'post', {
  'array|100': [{
    id: '@id',
    headline: "'@title",//标题
    text: "@cparagraph(10)",//内容
    answer: "@cparagraph(10, 20)",//答案
    grade: "@natural(60, 100)",//分数
    url: Random.image(),//图片
    "level|1-5": 1,//难度
  }]
})


// 提交答案
Mock.mock('/post_answer', 'post', {
  id: "1",
  user_id: "1",
  game_id: "1",
  result: "@integer(60, 100)",
  accomplish: "1",
})


// 得分事件
Mock.mock('/event', 'post', {
  'data|10': [{
    id: "@id",
    subject_id: "@id",
    username: "@cname",
    headline: "@title(1)",
    grade: "@natural(60, 100)",
    time: "@time",
    game_id: "@id",
  }]
})



