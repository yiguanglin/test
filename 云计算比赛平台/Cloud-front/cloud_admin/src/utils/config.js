// id 是你要打印的某个dom元素的id名
export function printExcel (id) {
  // 空页面
  let printStr = "<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head>"
  // 定义element-ui table组件的样式
  const tabStyle = `<style>
			table{width:100%;display:table-cell!important;box-sizing:border-box;}
			.el-table__header,.el-table__body,.el-table__footer{width:100%!important;border-collapse: collapse;text-align:center;}
			table,table tr th, table tr td { border:1px solid #ddd;color:#606266;word-wrap:break-word}
			table tr th,table tr td{padding:4mm 0mm;word-wrap:break-word }
			.el-table__body, tr td .cell{width:100%!important}
			.el-table th.gutter{display: none;}
			.el-table colgroup.gutter{display: none;}
      h1{text-align:center;}
			</style><body><h1>云计算比赛选手信息表</h1>`
  let content = ''
  // 获取名为传入id的 dom元素内的内容
  const str = document.getElementById(id).innerHTML
  // 拼接空页面+style样式+dom内容
  content = content + str
  printStr = printStr + tabStyle + content + '</body></html>'
  // 打开新页面
  const pwin = window.open('_blank')
  // 将内容赋值到新页面
  pwin.document.write(printStr)
  pwin.document.close()
  // 聚焦-不加focuse，在某些情况下，打印页面会有问题。
  pwin.focus()
  // 使用setTimeout，等页面dom元素渲染完成后再打印。
  setTimeout(() => {
    pwin.print() // 打印功能。 例如 window.print() 直接打印当前整个页面。
    pwin.close() // 关闭 打印创建的当前页面
  }, 500)
}
