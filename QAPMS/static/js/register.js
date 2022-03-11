// 我们采用的时ES6的语法
// 创建Vue对象 vm
let vm = new Vue({
    el: '#register', // 通过ID选择器找到绑定的HTML内容
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data: { // 数据对象
        // v-model
        username: '',
        EID:'',
        password: '',
        password2: '',
        email_address: '',
        email_code: '',
        email_code_tip: '获取邮箱验证码',
        send_flag: false, // 类比上厕所，send_flag就是锁，false表示门开，true表示门关

        // v-show
        error_name: false,
        error_EID:false,
        error_password: false,
        error_password2: false,
        error_email_address: false,
        error_email_code: false,

        // error_message
        error_name_message: '',
        error_EID_message:'',
        error_email_message:'',
        error_email_code_message: '',

    },
    methods: { // 定义和实现事件方法
        // 发送短信验证码
        send_email_code() {},
        //     // 避免恶意用户频繁的点击获取短信验证码的标签
        //     if (this.send_flag == true) { // 先判断是否有人正在上厕所
        //         return; // 有人正在上厕所，退回去
        //     }
        //     this.send_flag = true; // 如果可以进入到厕所，立即关门
        //
        //     // 校验数据：mobile，image_code
        //     this.check_email();
        //     if (this.error_email_address == true) {
        //         this.send_flag = false;
        //         return;
        //     }
        //
        //     let url = '/sms_codes/' + this.email_address + '&uuid=' + this.uuid;
        //     axios.get(url, {
        //         responseType: 'json'
        //     })
        //         .then(response => {
        //             if (response.data.code == '0') {
        //                 // 展示倒计时60秒效果
        //                 let num = 60;
        //                 let t = setInterval(() => {
        //                     if (num == 1) { // 倒计时即将结束
        //                         clearInterval(t); // 停止回调函数的执行
        //                         this.sms_code_tip = '获取短信验证码'; // 还原sms_code_tip的提示文字
        //                         this.generate_image_code(); // 重新生成图形验证码
        //                         this.send_flag = false;
        //                     } else { // 正在倒计时
        //                         num -= 1; // num = num - 1;
        //                         this.sms_code_tip = num + '秒';
        //                     }
        //                 }, 1000)
        //             } else {
        //                 if (response.data.code == '4001') { // 图形验证码错误
        //                     this.error_image_code_message = response.data.errmsg;
        //                     this.error_image_code = true;
        //                 } else { // 4002 短信验证码错误
        //                     this.error_sms_code_message = response.data.errmsg;
        //                     this.error_sms_code = true;
        //                 }
        //                 this.send_flag = false;
        //             }
        //         })
        //         .catch(error => {
        //             console.log(error.response);
        //             this.send_flag = false;
        //         })
        // },
        // 校验用户名
        check_username() {
            // 用户名是5-20个字符，[a-zA-Z0-9_-]
            // 定义正则
            let re = /^[a-zA-Z0-9 _-]{5,20}$/;
            // 使用正则匹配用户名数据
            if (re.test(this.username)) {
                // 匹配成功，不展示错误提示信息
                this.error_name = false;
            } else {
                // 匹配失败，展示错误提示信息
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            }


            // 判断用户名是否重复注册
            if (this.error_name == false) { // 只有当用户输入的用户名满足条件时才回去判断
                let url = '/username/' + this.username + '/count/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            // 用户名已存在
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            // 用户名不存在
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
        // 校验EID
        check_EID() {
            let re = /^[EH]{1}[0-9]{6}$/;
            if (re.test(this.EID)){
                this.error_EID=false;
            }else{
                this.error_EID=true;
                this.error_EID_message = '请输入正确的EID'
            }
                // 判断EID是否重复注册
            if (this.error_EID == false) { // 只有当用户输入的EID满足条件时才回去判断
                let url = '/EID/' + this.EID + '/count/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            // EID已存在
                            this.error_EID_message = 'EID已存在';
                            this.error_EID = true;
                        } else {
                            // 用户名不存在
                            this.error_EID = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
         // 校验密码
        check_password() {
            let re = /^[0-9A-Za-z\W\S]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 校验确认密码
        check_password2() {
            if (this.password != this.password2) {
                this.error_password2 = true;
            } else {
                this.error_password2 = false;
            }
        },
        // 校验邮箱
        check_email() {
            let re = /^[0-9a-zA-Z.]+@honeywell.com$/;
            if (re.test(this.email_address)) {
                this.error_email_address = false;
            } else {
                this.error_email_message = '您输入的邮箱格式不正确，请使用您的公司邮箱';
                this.error_email_address = true;
                    // 判断EMAIL是否重复注册
            if (this.error_email_address == false) { // 只有当用户输入的EMAIL满足条件时才回去判断
                let url = '/email/' + this.email_address + '/count/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            // 用户名已存在
                            this.error_email_address= 'email已存在';
                            this.error_email_address = true;
                        } else {
                            // 用户名不存在
                            this.error_email_address = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
                }
            }

        },

        // 校验邮箱验证码
        check_email_code(){
            if(this.email_code.length != 6){
                this.error_email_code_message = '请填写邮箱验证码';
                this.error_email_code = true;
            } else {
                this.error_email_code = false;
            }
        },
        // 监听表单提交事件
        on_submit() {
            this.check_username();
            this.check_EID();
            this.check_password();
            this.check_password2();
            this.check_email();
            this.check_email_code();

            // 在校验之后，注册数据中，只要有错误，就禁用掉表单的提交事件
            if (this.error_name == true || this.error_password == true || this.error_password2 == true || this.error_EID == true || this.error_email_address == true || this.error_email_code == true) {
                // 禁用掉表单的提交事件
                window.event.returnValue = false;

            }
        },
    }
});