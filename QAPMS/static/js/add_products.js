let app = new Vue({
    el:'#add_products',
    delimiters: ['[[', ']]'],
    data:{
        //v-model
        pid:'',
        SKU_list:[],
        SKU_name_list:[],
        new_SKU:'',
        new_SKU_type:1,
        new_SKU_name:'',
        new_SKU_desc:'',
        //v-show
        error_SKU:false,
        //error-message
        error_SKU_msg:'',
    },

    methods:{
        SKU_check:function (){
            this.error_SKU=false;
            if (!this.new_SKU){
                this.error_SKU = true;
                this.error_SKU_msg = '请输入设备型号'
                return
            }
            if (this.SKU_list.length !== 0){
                // js没有python的for in 函数，只能通过循环获取字典中所有SKU的值，通过include来判断
                for (let x in this.SKU_list){
                  this.SKU_name_list.push(this.SKU_list[x].SKU);
                }
                if (this.SKU_name_list.includes(this.new_SKU)){
                this.error_SKU = true;
                this.error_SKU_msg = '设备已存在'
                this.SKU_name_list=[];
                }
            }
        },
        add_SKU:function(){
            if(this.error_SKU){alert('请检查输入的设备型号')}
            else {
                this.SKU_list.push({project:this.project_name,
                                    SKU:this.new_SKU,
                                    SKU_type:this.new_SKU_type,
                                    SKU_name:this.new_SKU_name,
                                    SKU_desc:this.new_SKU_desc});
                this.new_SKU='';
                this.new_SKU_name='';
                this.new_SKU_desc='';
                this.error_SKU = false;
            }
        },
        deleteSKU:function(index){this.SKU_list.splice(index,1)},
        product_save:function(){
            let url=window.location.href
            axios.post(url, this.SKU_list,{
                headers: {'X-CSRFToken':getCookie('csrftoken')},
                responseType: 'json'
            })
                .then(res=>{ console.log(res) })
                .catch(error=>{console.log(error.response)})
        },
    }

})