let app= new Vue({
    el: '#index',
    delimiters: ['[[', ']]'],
    data: {
        username: '',
        change_password:'',
    },
    mounted:function (){
        this.username=getCookie('username');
        this.change_password='/change_password/' + getCookie('EID');
    }
})

