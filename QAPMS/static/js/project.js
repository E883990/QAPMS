let app = new Vue({
    el: '#project',
    delimiters: ['[[', ']]'],
    data: {
        //先处理Django变量
        SKU_list: JSON.parse(JSON.stringify(SKUs)),
        PG_shows: JSON.parse(JSON.stringify(PG_show)),
        p_id: JSON.parse(JSON.stringify(project_id)),
        url: '',
        //v-model:
        SKU_check_list:[],
        editing_SKU_index:'',
        form_SKU: {
            id:'',
            SKU: '',
            product_type: '',
            SKU_name: '',
            SKU_desc: '',
        },
        project_name: '',
        project_desc: '',
        QAPL: '',
        project_m: '',
        EPL: '',
        product_m: '',
        pstart: '',
        pend: '',
        practical_start: '',
        practical_end: '',
        new_SKU_list:[],
        new_SKU:'',
        new_SKU_type:1,
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
        new_plan:false,
        new_practical:false,
        //设备
        SKU_add:true,
        SKU_save:false,
        add_SKU_show:false,
        error_SKU:false,
        added_SKU_show:false,
        show_edit_table: false,
        //修改后展示：
        update_name_show: false,
        update_desc_show: false,
        update_members_show:false,
        // 错误码
        error_project_name_msg: '',
        error_update_members_msg:'',
        error_SKU_msg:'',
        SKU_error_msg:'',
        // PG4页面
            // V-model
        PG4_pstart:'',
        PG4_pend:'',
        PG4_practical_start:'',
        PG4_practical_end:'',
            // v-show
        PG4_p_input:false,
        PG4_new_plan:false,
        PG4_plan_change:true,
        PG4_plan_save:false,
        PG4_practical_input:false,
        PG4_new_practical:false,
        PG4_practical_change:true,
        PG4_practical_save:false,
    //  FW 功能
        //  V-model

        //  V-show
        show_FW_upload_table:false,
    },
    mounted:function (){
       this.url= '/project/'+ this.p_id + '/update/';
       // alert(this.url);
       switch (this.PG_shows){
           case "PG1":
               this.show_PG1();
               break;
           case "PG2":
               this.show_PG2();
               break;
           case "PG3":
               this.show_PG3();
               break;
           case "PG4":
               this.show_PG4();
               break;
           case "PG5":
               this.show_PG5();
               break;
           case "PG6":
               this.show_PG6();
               break;
           default:
               this.show_PG1();
               break
       }
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
        // 展示修改设备界面
        show_edit_SKU(index){
            this.show_edit_table = true;
            this.error_SKU=false;
            this.editing_SKU_index = index.toString();
            // 只获取要编辑的数据
            this.form_SKU = JSON.parse(JSON.stringify(this.SKU_list[index]));
        },
        // 校验SKU必须输入,其他可以为空
        check_SKU(){
            if (!this.form_SKU.SKU) {
                this.error_SKU = true;
                this.SKU_error_msg='此处不得为空'
            }
        },
        // 保存设备的修改
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
        // 展示添加设备界面
        show_addSKU_form:function (){
            this.add_SKU_show=true;
            if (this.new_SKU_list.length!==0){
                this.added_SKU_show=true;
            }
        },
        // 取消添加
        cancel_add:function (){
            this.add_SKU_show=false;
            this.added_SKU_show=false
        },
        // 设备输入检查，只检查型号
        new_SKU_check:function (){
            //先将错误码取消，否则失败一次永远无法添加
            this.error_SKU = false;
            //  判断需要添加的设备是否重名
            // 1.检查SKU_list设备列表:
                 // js没有python的for in 函数，只能通过循环获取字典中所有SKU的值，通过include来判断
            if (this.SKU_list.length !== 0){
                for (let x in this.SKU_list){
                    this.SKU_check_list.push(this.SKU_list[x].SKU);
                }
            }
             // 2.检查已添加的设备列表:
            if (this.new_SKU_list.length !== 0){
                for (let x in this.new_SKU_list){
                    this.SKU_check_list.push(this.new_SKU_list[x].SKU);
                }
            }
            //  3.进行检查
            if (this.SKU_check_list.includes(this.new_SKU)){
                    this.error_SKU = true;
                    this.error_SKU_msg = '设备已存在，请检查设备列表'
                }
            // 4.清空检查表，防止重复添加
            this.SKU_check_list=[];
        },
        add_SKU:function (){
        // 1.检查设备是否为空
            if(!this.new_SKU){
                this.error_SKU = true;
                this.error_SKU_msg = '请输入设备名'
            }
        // 2.展示添加的设备框，
            if(!this.added_SKU_show){
                this.added_SKU_show=true;
            }
        // 3.检查是否有错误
            if(this.error_SKU){alert('请检查输入的设备型号')}
        // 4.将设备加入新设备列表
            else {
                this.new_SKU_list.push({SKU:this.new_SKU,
                                        SKU_type:this.new_SKU_type,
                                        SKU_name:this.new_SKU_name,
                                        SKU_desc:this.new_SKU_desc});
                this.new_SKU='';
                this.new_SKU_name='';
                this.new_SKU_desc='';
                this.error_SKU = false;
            }
        },
        deleteSKU:function(index){this.new_SKU_list.splice(index,1)},
        product_save:function (){
            let url='/addproducts/'+this.p_id.toString()+'/';
            axios.post(url, this.new_SKU_list,{
                headers: {'X-CSRFToken':getCookie('csrftoken')},
                responseType: 'json'
            })
                .then(res=>{
                        console.log(res);
                        location.reload(true);
                })
                .catch(error=>{console.log(error.response)})
        },
        change_plan:function (){
            this.p_input=true;
            this.plan_change=false;
            this.plan_save=true;
            this.new_plan=false;
        },
        save_plan:function (){
            this.p_input=false;
            this.plan_change=true;
            this.plan_save=false;
            // 1.判断输入是否为空
            if(this.pstart==='' || this.pend===''){
                alert('未输入数据')
            }
            // 2.发送不为空的数据
            else {
                this.new_plan=true;
                let data = {'pstart':this.pstart,'pend':this.pend};
                axios.put(this.url, data ,
                    {headers: {'X-CSRFToken':getCookie('csrftoken')},
                     responseType: 'json'})
                .then(res=>{
                    alert(this.url)
                    console.log(res.data);
                })
                .catch(error=>{
                    alert('出错了');
                    console.log(error.response);
                })
            }
        },
        change_practical:function (){
            this.practical_input=true;
            this.practical_change=false;
            this.practical_save=true;
            this.new_practical=false;
        },
        save_practical:function (){
            this.practical_input=false;
            this.practical_change=true;
            this.practical_save=false;
            // 1.判断输入是否为空
            if(this.practical_start==='' || this.practical_end===''){
                alert('未输入数据')
            }
            // 2.发送不为空的数据
            else {
                this.new_practical=true;
                let data = {'practical_start':this.practical_start,'practical_end':this.practical_end};
                axios.put(this.url, data ,
                    {headers: {'X-CSRFToken':getCookie('csrftoken')},
                     responseType: 'json'})
                .then(res=>{
                    console.log(res.data);
                })
                .catch(error=>{
                    alert('出错了');
                    console.log(error.response);
                })
            }
        },
        PG4_change_plan:function (){
            this.PG4_p_input=true;
            this.PG4_new_plan=false;
            this.PG4_plan_change=false;
            this.PG4_plan_save=true;
        },
        PG4_save_plan:function (){
             // 1.判断输入是否为空
            if(this.PG4_pstart==='' || this.PG4_pend===''){
                alert('未输入数据')
            }
            // 2.发送不为空的数据
            else {
                let data = {'PG4_pstart':this.PG4_pstart,'PG4_pend':this.PG4_pend};
                axios.put(this.url, data ,
                    {headers: {'X-CSRFToken':getCookie('csrftoken')},
                     responseType: 'json'})
                .then(res=>{
                    console.log(res.data);
                    this.PG4_p_input=false;
                    this.PG4_new_plan=true;
                    this.PG4_plan_change=true;
                    this.PG4_plan_save=false;
                })
                .catch(error=>{
                    alert('出错了');
                    console.log(error.response);
                })
            }
        },
        PG4_change_practical:function (){
            this.PG4_practical_input=true;
            this.PG4_new_practical=false;
            this.PG4_practical_change=false;
            this.PG4_practical_save=true;
        },
        PG4_save_practical:function (){
              // 1.判断输入是否为空
            if(this.PG4_practical_start==='' || this.PG4_practical_end===''){
                alert('未输入数据')
            }
            // 2.发送不为空的数据
            else {
                let data = {'PG4_practical_start':this.PG4_practical_start,'PG4_practical_end':this.PG4_practical_end};
                axios.put(this.url, data ,
                    {headers: {'X-CSRFToken':getCookie('csrftoken')},
                     responseType: 'json'})
                    .then(res=>{
                    console.log(res.data);
                    this.PG4_practical_input=false;
                    this.PG4_new_practical=true;
                    this.PG4_practical_change=true;
                    this.PG4_practical_save=false;
                })
                .catch(error=>{
                    alert('出错了');
                    console.log(error.response);
                })
            }
        },
    }
})