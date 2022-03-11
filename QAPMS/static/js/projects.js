let vm = new Vue({
    el: '#projects', // 通过ID选择器找到绑定的HTML内容
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data: {
        show:'展开',
        list_show:false,
    },
    methods:{
        change_status(){
            if (this.list_show){
                this.list_show = false;
                this.show='展开';
            }
            else {
                this.list_show = true;
                this.show='收起';

            }

        },
    }
})
