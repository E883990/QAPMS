let app = new Vue({
    el: '#project',
    delimiters: ['[[', ']]'],
    data: {
        url: window.location.href + 'update/',
        SKU_list: JSON.parse(JSON.stringify(SKUs)),
        show_edit_table: false,
        p_id:JSON.parse(JSON.stringify(project_id)),
        form_SKU: {
            id:'',
            SKU: '',
            product_type: '',
            SKU_name: '',
            SKU_desc: '',
        },
        editing_SKU_index:'',
        //v-model:
        project_name: '',
        project_desc: '',
        QAPL: '',
        project_m: '',
        EPL: '',
        product_m: '',
        plan_start: '',
        plan_end: '',
        practical_start: '',
        practical_end: '',
        new_SKU:'',
        new_SKU_type:'',
        new_SKU_list:'',
        new_SKU_name:'',
        new_SKU_desc:'',
        //v-show:
        PG1: true,
        PG2: false,
        PG3: false,
        PG4: false,
        PG5: false,
        PG6: false,
        //button 和输入框
        //项目名字
        name_input: false,
        name_change: true,
        name_save: false,
        error_project_name: false,
        //项目描述
        desc_input: false,
        desc_change: true,
        desc_save: false,
        error_project_desc:false,
        //项目成员
        members_input: false,
        members_change: true,
        members_save: false,
        error_members:false,
        //计划
        p_input: false,
        practical_input: false,
        plan_change: true,
        plan_save: false,
        practical_change: true,
        practical_save: false,
        project_change: false,
        project_save: true,
        project_submit: false,
        //设备
        SKU_add:true,
        SKU_save:false,
        add_SKU_show:false,
        error_SKU:false,
        //修改后展示：
        update_name_show: false,
        update_desc_show: false,
        update_members_show:false,
        // 错误码
        error_project_name_msg: '',
        error_update_members_msg:'',
        error_SKU_msg:'',
        SKU_error_msg:'',
    },
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
        change_name:function (){
            this.name_input=true;
            this.name_save=true;
            this.name_change=false;
            this.update_name_show=false;
        },
        save_name:function (){
            this.name_input=false;
            this.name_save=false;
            this.name_change=true;
            let data={'project_name':this.project_name}
            if (!this.project_name){
                this.error_project_name=true;
                this.error_project_name_msg='没有做任何修改'
                return
            }
            axios.put(this.url, data ,{responseType: 'json'})
                .then(res=>{
                    console.log(res.data);
                    if (res.data.update_name_show){this.update_name_show = true;}
                    if(res.data.error_project_name_msg)
                    {this.error_project_name =true;
                    this.error_project_name_msg='项目名重复';}
                })
                .catch(error=>{
                    alert('出错了');
                    console.log(error.response);
                })
        },
        change_desc:function (){
            this.desc_input=true;
            this.desc_change=false;
            this.desc_save=true;
            this.update_desc_show=false;
        },
        save_desc:function (){
            this.desc_input=false;
            this.desc_change=true;
            this.desc_save=false;
            let data={'project_desc':this.project_desc}
            if (!this.project_desc){
                this.error_project_desc=true;
                this.error_project_name_msg='没有做任何修改'
                return
            }
            axios.put(this.url, data, {responseType: 'json'})
                .then(res=>{
                    if (res.data.update_desc_show){
                        this.update_desc_show=true;
                    }
                    console.log(res.data);
                })
                .catch(error=>{
                    alert('出错了');
                    console.log(error.response);
                })
        },
        change_members:function (){
            this.members_input=true;
            this.members_change=false;
            this.members_save=true;
            this.update_members_show=false;
        },
        save_members:function (){
            this.members_change=true;
            this.members_input=false
            this.members_save=false;
            let data={'project_manager':this.project_m,'product_manager':this.product_m,
                       'QAPL':this.QAPL,'EPL':this.EPL}
            if (!this.project_m && !this.product_m && !this.QAPL && !this.EPL){
                this.error_members=true;
                this.error_update_members_msg='没有做任何修改'
                return
            }
            axios.put(this.url, data ,{responseType: 'json'})
                .then(res=>{
                    if (res.data.update_members_show){
                        this.update_members_show=true;
                        this.error_members=false;
                    }
                    else{this.error_members=true}
                    console.log(res.data);
                })
                .catch(error=>{
                    alert('出错了');
                    console.log(error.response);
                })
        },
        show_addSKU_form:function (){
            this.add_SKU_show=true;
        },
        cancel_add:function (){
            this.add_SKU_show=false;
        },
        show_edit_SKU(index){
            this.show_edit_table = true;
            this.error_SKU=false;
            this.editing_SKU_index = index.toString();
            // 只获取要编辑的数据
            this.form_SKU = JSON.parse(JSON.stringify(this.SKU_list[index]));
        },
        // 校验SKU必须输入
        check_SKU(){
            if (!this.form_SKU.SKU) {
                this.error_SKU = true;
                this.SKU_error_msg='此处不得为空'
            }
        },
        save_SKU:function (){
            if(this.error_SKU){alert('信息填写有误！');}
            else {
            //    发送修改请求
                let url='/addproducts/'+this.p_id.toString()+'/';
                axios.put(url, this.form_SKU, {
                        headers: {'X-CSRFToken':getCookie('csrftoken')},
                        responseType: 'json'})
                     .then(response => {
                         // 注意：0 == '';返回true; 0 === '';返回false;
                            if (response.data.code == '0') {
                                this.SKU_list[this.editing_SKU_index] = response.data.new_product;
                                this.show_edit_table = false;}
                            else if(response.data.code == '5006'){
                                this.error_SKU=true;
                                this.SKU_error_msg=response.data.errmsg;
                            }
                            else {alert(response.data.errmsg);}
                        })
                     .catch(error => {alert(error.response);})
            }
        },
        change_plan:function (){},
        save_plan:function (){},
        change_practical(){},
        save_practical(){},
        add_SKU(){}
    }
})