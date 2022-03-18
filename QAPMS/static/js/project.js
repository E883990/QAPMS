let app = new Vue({
    el: '#project',
    delimiters: ['[[', ']]'],
    data:{
        //v-model:
        project_name:'',
        project_desc:'',
        QAPL:'',
        project_manager:'',
        EPL:'',
        product_manager:'',
        plan_start:'',
        plan_end:'',
        practical_start:'',
        practical_end:'',
        SKUs:[],
        //v-show:
        PG1:true,
        PG2:false,
        PG3:false,
        PG4:false,
        PG5:false,
        PG6:false,
    },
    // mounted:function (){
    //     let url=window.location.href
    //     axios.get(url, {responseType: 'json'})
    //         .then(res=>{
    //             this.project_name=response.data.project_name;
    //             this.project_desc=response.data.project_desc;
    //             this.QAPL=response.data.QAPL;
    //             this.project_manager=response.data.project_manager;
    //             this.EPL=response.data.EPL;
    //             this.product_manager=response.data.product_manager;
    //             this.plan_start=response.data.plan_start;
    //             this.plan_end=response.data.plan_end;
    //             this.practical_start=response.data.practical_start;
    //             this.practical_end=response.data.practical_end;
    //             this.SKUs=response.data.SKUs;
    //         })
    //         .catch(error=>{console.log(error.response)})
    // },
    methods:{
        show_PG1:function (){
            this.PG1 = true;
            this.PG2 = false;
            this.PG3 = false;
            this.PG4 = false;
            this.PG5 = false;
            this.PG6 = false;
        },
        show_PG2:function (){
            this.PG1 = false;
            this.PG2 = true;
            this.PG3 = false;
            this.PG4 = false;
            this.PG5 = false;
            this.PG6 = false;
        },
        show_PG3:function (){
            this.PG1 = false;
            this.PG2 = false;
            this.PG3 = true;
            this.PG4 = false;
            this.PG5 = false;
            this.PG6 = false;
        },
        show_PG4:function (){
            this.PG1 = false;
            this.PG2 = false;
            this.PG3 = false;
            this.PG4 = true;
            this.PG5 = false;
            this.PG6 = false;
        },
        show_PG5:function (){
            this.PG1 = false;
            this.PG2 = false;
            this.PG3 = false;
            this.PG4 = false;
            this.PG5 = true;
            this.PG6 = false;
        },
        show_PG6:function (){
            this.PG1 = false;
            this.PG2 = false;
            this.PG3 = false;
            this.PG4 = false;
            this.PG5 = false;
            this.PG6 = true;
        },
    }
})