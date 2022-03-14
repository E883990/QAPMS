let app = new Vue({
    el: '#cpwd',
    // 修改Vue变量的读取语法
    delimiters: ['[[', ']]'],
    data: {
        //v-bind
        submit_color: 'input_submit_forbid',
        // v-model
        new_password: '',
        new_password2: '',
        EID: '',
        // v-show
        error_new_password: false,
        error_password2: false,
    },
    mounted: function(){
        this.EID=getCookie('EID');
    },
    methods: {
        check_new_password() {
            let re = /^[^\s]{8,20}$/;
            if (re.test(this.new_password)) {
                this.error_new_password = false;
            } else {
                this.error_new_password = true;
            }
        },
        check_new_password2() {
            if (this.new_password == this.new_password2) {
                this.error_password2 = false;
            } else {
                this.error_password2 = true;
            }
            if (this.error_password2 == false && this.new_password2 != ''){
                this.submit_color = 'input_submit';
            }
        },
        on_submit() {
            this.check_password();
            this.check_new_password();
            this.check_new_password2();
            // 在校验之后，注册数据中，只要有错误，就禁用掉表单的提交事件
            if (this.error_old_pwd == true || this.error_new_password == true || this.error_password2 == true) {
                // 禁用掉表单的提交事件
                window.event.returnValue = false;
            }
        },
    }
})