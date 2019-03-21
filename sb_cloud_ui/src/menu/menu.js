let menu = {};

/**
 * 首页
 * @type {{name: string, path: string, icon: string}}
 */
menu.home = {
  name: '首页',
  path: '/',
  icon: 'fa fa-tachometer',
};


/**
 * 资源管理
 * @type {{name: string, icon: string, children: {}}}
 */
menu.resource_manager = {
  name: '资源管理',
  icon: 'fa fa-th',
  children: {}
};
let resource_manager = menu.resource_manager.children;

resource_manager.host = {
  name: '云主机',
  path: '/host_list',

};
resource_manager.storage = {
  name: '云存储',
  path: '/storage',
};
resource_manager.sql = {
  name: '云数据库',
  path: '/sql',
};
resource_manager.vpc = {
  name: '专有网络',
  path: '/vpc',
};
resource_manager.balanced = {
  name: '负载均衡',
  path: '/balanced',
};

/**
 * 备份管理
 * @type {{name: string, icon: string, children: {}}}
 */
menu.backup_manager = {
  name: '备份管理',
  icon: 'fa fa-file-text-o',
  children: {}
};

let backup_manager = menu.backup_manager.children;

backup_manager.whole = {
  name: '概览',
  path: '/whole',
};
backup_manager.backup = {
  name: '备份',
  path: '/backup',
};
backup_manager. resume = {
  name: '恢复',
  path: '/resume',
};
backup_manager.policy = {
  name: '策略',
  path: '/policy',
};


/**
 * 用户管理
 * @type {{name: string, icon: string, children: {}}}
 */
menu.user_manage = {
  name: '账户管理',
  path: '/account',
  icon: 'fa fa-user-circle-o',
};
// menu.user_manage = {
//   name: '用户管理',
//   icon: 'fa fa-user-circle-o',
//   children: {}
// };
// let UserManage = menu.user_manage.children;
//
// UserManage.user = {
//   name: '用户列表',
//   path: '/user_manage',
// };
//
//
// /**
//  * 分类管理
//  * @type {{name: string, icon: string, children: {}}}
//  */
// menu.category_manage = {
//   name: '分类管理',
//   icon: 'fa fa-sitemap',
//   children: {}
// };
// let CategoryManage = menu.category_manage.children;
//
// CategoryManage.category = {
//   name: '分类列表',
//   path: '/category_manage',
// };
//
//
//
// menu.permission_manage = {
//   name: '权限管理',
//   icon: 'fa fa-qrcode',
//   children: {}
// };
// let PermissionManage = menu.permission_manage.children;
//
// PermissionManage.role = {
//   name: '角色管理',
//   path: '/role_manage',
// };
//
// PermissionManage.permission = {
//   name: '权限列表',
//   path: '/permission_list',
// };
//
export default menu;

// if(process.env.NODE_ENV=='development'){
//
//   menu.development_tools = {
//     name: '开发工具',
//     icon: 'fa fa-wrench',
//     children: {}
//   };
//
//   let DevelopmentTools = menu.development_tools.children;
//
//   DevelopmentTools.code = {
//     name: '构建代码',
//     path: '/build_code',
//   };
//
// }
