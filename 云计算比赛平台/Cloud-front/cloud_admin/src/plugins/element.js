import Vue from 'vue'
import {
  Button,
  Message,
  MessageBox,
  Card,
  Form,
  FormItem,
  Input,
  Container,
  Header,
  Aside,
  Main,
  Menu,
  MenuItem,
  MenuItemGroup,
  Submenu,
  Breadcrumb,
  BreadcrumbItem,
  Row,
  Col,
  Table,
  TableColumn,
  Alert,
  Dialog,
  Select,
  Option,
  Drawer,
  Divider
} from 'element-ui'
Vue.use(Button)
Vue.use(Card)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Menu)
Vue.use(MenuItem)
Vue.use(MenuItemGroup)
Vue.use(Submenu)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Row)
Vue.use(Table)
Vue.use(Col)
Vue.use(TableColumn)
Vue.use(Alert)
Vue.use(Dialog)
Vue.use(Select)
Vue.use(Option)
Vue.use(Drawer)
Vue.use(Divider)
Vue.prototype.$message = Message
Vue.prototype.$confirm = MessageBox.confirm
