let vm = new Vue({
      // 表示ID为app的元素
      el: '#register',
      delimiters: ['[[',']]'],
      data: {
            //v-model
            username:'',
            EID:'',
            password:'',
            password2:'',
            email:'',

            //v-show
            error_name: false,
            error_EID: false,
            error_password: false,
            error_password2: false,
            error_email: false,
            error_email_code: false,

            //errormessage
            error_name_message: '',
            error_EID_message: '',
            error_password_message: '',
            error_password2_message: '',
            error_email_message: '',
            email_code_errmsg: '',
      },
      //v-model
      // mounted(){},
      methods:{
            //检查用户名
            check_username(){
                  //用户名是5-30个字母数字或空格-_
                  //定义正则
                  let re = /^[a-zA-Z0-9_\s]{5,30}$/;
                  //使用正则匹配数据
                  if(re.test(this.username)){
                        //匹配成功就不展示错误数据
                        this.error_name = false;
                        }
                  else {
                        //匹配失败就展示错误数据
                        this.error_name_message = '请输入5-30个字符的用户名，只可以含_-和空格';
                        this.error_name = true;
                        }
                  },
            // //检查EID
            // check_EID(){},
            // //检查密码
            // check_password(){},
            // //检查确认密码
            // check_password2(){},
            // //检查邮箱
            // check_email(){},
            // //检查邮箱验证码
            // check_email_code(){},
            // //发送邮箱验证码
            // send_email_code(){},
      }
    })