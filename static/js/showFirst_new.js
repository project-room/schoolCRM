$(function () {
    /**日期显示 */
    laydate.render({
        elem: '#dateStart',
        format: 'yyyy-MM-dd'
    });
    laydate.render({
        elem: '#dateEnd',
        format: 'yyyy-MM-dd'
    });

    laydate.render({
        elem: '#dateLeft',
        format: 'yyyy-MM-dd'
    });

    laydate.render({
        elem: '#dateRight',
        format: 'yyyy-MM-dd'
    });
    laydate.render({
        elem: '#moneyDate',
        format: 'yyyy-MM-dd'
    });


    /**教师信息里的密码修改 */

    $('.numberSetting .correct').click(function (event) {
        // event.stopPropagation();
        $('#smallcover').show()
        $("#smallmodal").show()

    })

    $('#smallmodal .smallModal_content .smallButton').find('input[value="取消"]').click(function () {
        $('#smallcover').hide()
        $("#smallmodal").hide()
    })

    /**改变页面宽度 */
    $('.mainContent').width($('body').width() - 200);
    $('.contentHead').width($('body').width() - 200);
    $('.studentContent').width($('body').width() - 200);
    $('.setting').width($('body').width() - 200);
    $('.classEdit').width($('body').width() - 200);
    $('.studentDetail').width($('body').width() - 200);
    $('.studentEdit').width($('body').width() - 200);
    $('.teacherDetail').width($('body').width() - 200);
    $('.teacherEdit').width($('body').width() - 200);
    $('.addList').width($('body').width() - 200);
    $('.addNumber').width($('body').width() - 200);
    $('.editNumber').width($('body').width() - 200);
    $('.registrationInformation').width($('body').width() - 200);
    $('.registrationAddInfomation').width($('body').width() - 200);
    $('.classrecycleContent,.studentrecycleContent,.teacherrecycleContent,.peoplerecycleContent').width($('body').width() - 200);
    $('.baseSettingInformation').width($('body').width() - 200);
    $('.baseContent').width($('.baseSettingInformation').width() - 210);
    $('.studentDetail .content').width($('.studentDetail').width()+100);
    $('.teacherDetail .content').width($('.teacherDetail').width()+100);
    



    $('#basecover').height($('body').height())
    $('.content').height($('.sideContent').height()-120)
    // $('.sideContent').height($('body').height())


    // $('.leftSide').height($('body').height())
    $('.baseLeftSide').height($('body').height()-20)
    // $('.studentContent').height($('body').height()-50);


    /**悬浮div */
    var list = $('.mainShow ul li')
    var studentLis = $('.studentContentMain ul li')
    var classrecycleList = $('.classrecycleContent ul li')
    var studentrecycleList = $('.studentrecycleContent ul li')
    var teacherList = $('.teacherrecycleContent ul li')
    var peopleList = $('.peoplerecycleContent ul li')


    function operate(a) {
        for (var i = 0; i < a.length; i++) {
            $(a[i]).hover(function () {
                $(this).find('a').css('text-decoration', 'none')
                $(this).find(".operate").css('display', "inline-block").css("cursor", "pointer").css('zIndex', 9999)
            }, function () {
                $(this).find(".operate").hide()
            });

            /**每个li后面的悬浮div */
            $(a[i]).find(".operate .delete").click(function () {
                $(this).parent().parent().remove()
            })
        }
    }

    function operateTree(a) {
        for (var i = 0; i < a.length; i++) {
            $(a[i]).hover(function () {
                $(this).find(".operate").css('display', "inline-block").css("cursor", "pointer")
            }, function () {
                $(this).find(".operate").hide()
            });
        }
    }
    operate(list);
    operate(studentLis);
    operateTree(classrecycleList);
    operateTree(studentrecycleList);
    operateTree(teacherList);
    operateTree(peopleList);


    /** 关闭弹框遮罩 */
    function showHide() {
        $('#cover').hide()
        $("#modal").hide()
    }

    function smallshowHide() {
        $('#smallcover').hide()
        $("#smallmodal").hide()
    }

    function studentHide() {
        $('#studentmodal').hide()
        $('#studentcover').hide()
    }

    function teacherHide() {
        $('#teachermodal').hide()
        $('#teachercover').hide()
    }

    function addHide() {
        $('#addcover').hide()
        $('#addmodal').hide()
    }

    function studentaddHide() {
        $('#studentaddcover').hide()
        $('#studentaddmodal').hide()
    }

    function teacheraddHide() {
        $('#teacheraddcover').hide()
        $('#teacheraddmodal').hide()
    }

    function editHide() {
        $('#editcover').hide()
        $('#editmodal').hide()
    }

    function editstudentHide() {
        $('#edistudentcover').hide()
        $('#editstudentmodal').hide()
    }

    function editteacherHide() {
        $('#teachereditcover').hide()
        $('#teachereditmodal').hide()
    }
    showHide();
    smallshowHide();
    studentHide();
    teacherHide();
    addHide();
    studentaddHide();
    teacheraddHide();
    editHide();
    editstudentHide();
    editteacherHide();
    $("#close").click(function () {
        showHide();
    })
    $("#studentclose").click(function () {
        studentHide();
    })
    $("#teacherclose").click(function () {
        teacherHide();
    })
    $("#smallclose").click(function () {
        smallshowHide();
    })

    $("#addclose").click(function () {
        addHide();
    })
    $('#studentaddclose').click(function () {
        studentaddHide();
    })
    $('#editclose').click(function () {
        editHide();
    })
    $('#editstudentclose').click(function () {
        editstudentHide();
    })
    $('#teachereditclose').click(function () {
        editteacherHide();
    })
    /**顶层弹框的关闭 */
    $('#Topmodal #Topclose').click(function () {
        $('#Topcover').css('display', 'none');
        $('#Topmodal').css('display', 'none')
    })



    //显示弹框遮罩
    var tiaoshi = $(".tiaoshi .paddingLeft");
    var studentBig = $('.studentBig .paddingLeft');
    var teacherBig = $('.teacherNew .paddingLeft');
    var comback = $('.recycle .operate');
    var re_button = $('.recycle .re_button')

    function smallshow(b) {
        b.children().click(function () {
            $('#smallcover').show()
            $("#smallmodal").show()
        })
    }
    smallshow(comback);
    smallshow(re_button);

    /**导出 */
    tiaoshi.find('input[value="导出"]').click(function () {
        $('#cover').show()
        $("#modal").show()
    })
    studentBig.find('input[value="导出"]').click(function () {
        $('#studentcover').show()
        $("#studentmodal").show()
    })
    teacherBig.find('input[value="导出"]').click(function () {
        $('#teachercover').show()
        $("#teachermodal").show()
    })

    /**添加 */
    tiaoshi.find('input[value="添加"]').click(function () {
        $('#addcover').show()
        $("#addmodal").show()
    })
    // studentBig.find('input[value="添加"]').click(function () {
    //     $('#studentaddcover').show()
    //     $('#studentaddmodal').show()
    // })
    // teacherBig.find('input[value="添加"]').click(function () {
    //     $('#teacheraddcover').show()
    //     $('#teacheraddmodal').show()
    // })

    /**编辑 */
    tiaoshi.find('input[value="编辑"]').click(function () {
        // $('#editcover').show()
        // $("#editmodal").show()
        $('.tiaoshi .contentHead').css('display', 'none');
        $('.tiaoshi .mainContent').css('display', 'none')
        $('.tiaoshi .classEdit').css('display', 'block')
    })
    studentBig.find('input[value="编辑"]').click(function () {
        // $('#edistudentcover').show()
        // $("#editstudentmodal").show()
        $('.studentBig .contentHead').css('display', 'none');
        $('.studentBig .studentContent').css('display', 'none')
        $('.studentBig .studentEdit').css('display', 'block')
    })
    studentBig.find('input[value="添加"]').click(function () {
        // $('#edistudentcover').show()
        // $("#editstudentmodal").show()
        $('.studentBig .contentHead').css('display', 'none');
        $('.studentBig .studentContent').css('display', 'none')
        $('.studentBig .addList').css('display', 'block')
    })

    teacherBig.find('input[value="编辑"]').click(function () {
        $('.teacherNew .contentHead').css('display', 'none');
        $('.teacherNew .mainContent').css('display', 'none')
        $('.teacherNew .teacherEdit').css('display', 'block')
    })
    teacherBig.find('input[value="添加"]').click(function () {
        $('.teacherNew .contentHead').css('display', 'none');
        $('.teacherNew .mainContent').css('display', 'none')
        $('.teacherNew .addList').css('display', 'block')
    })



    /**展示左边导航的背景图 */
    var backgroundList = $('.leftSide .sideNav ul li')
    var arr = ['class01.png', 'student01.png', 'teacher01.png', 'setting01.png', 'huishou01.png']

    function getResult(a, b) {
        if (a.length === b.length) {
            for (var i = 0; i < a.length; i++) {
                a[i].style.background = "url('../../img/" + b[i] + "') 20px center no-repeat";
            }
        }
    }
    getResult(backgroundList, arr);


    for (var k = 0; k < backgroundList.length; k++) {


        $(backgroundList[0]).click(function () {
            background();
            $('.sideContent .tiaoshi').css('display', 'block');
            $(this).css('background', "url('../../img/class.png') 20px center no-repeat").find('a').css('color', '#fcb636');
        })
        $(backgroundList[1]).click(function () {
            background();
            $('.sideContent .studentBig').css('display', 'block');
            $(this).css('background', "url('../../img/student.png') 20px center no-repeat").find('a').css('color', '#fcb636');
        })
        $(backgroundList[2]).click(function () {
            background();
            $('.sideContent .teacherNew').css('display', 'block');
            $(this).css('background', "url('../../img/teacher.png') 20px center no-repeat").find('a').css('color', '#fcb636');
        })
        $(backgroundList[3]).click(function () {
            background();
            $('.sideContent .numberSetting').css('display', 'block');
            $(this).css('background', "url('../../img/setting.png') 20px center no-repeat").find('a').css('color', '#fcb636');
        })
        $(backgroundList[4]).click(function () {
            background();
            $('.sideContent .recycle').css('display', 'block');
            $(this).css('background', "url('../../img/huishou.png') 20px center no-repeat").find('a').css('color', '#fcb636');
        })
    }

    function background() {
        $(backgroundList[0]).css('background', "url('../../img/class01.png') 20px center no-repeat").find('a').css('color', '#808080');
        $(backgroundList[1]).css('background', "url('../../img/student01.png') 20px center no-repeat").find('a').css('color', '#808080');
        $(backgroundList[2]).css('background', "url('../../img/teacher01.png') 20px center no-repeat").find('a').css('color', '#808080');
        $(backgroundList[3]).css('background', "url('../../img/setting01.png') 20px center no-repeat").find('a').css('color', '#808080');
        $(backgroundList[4]).css('background', "url('../../img/huishou01.png') 20px center no-repeat").find('a').css('color', '#808080');


        // $('.sideContent .tiaoshi').css('display', 'none');
        // $('.sideContent .studentBig').css('display', 'none');
        // $('.sideContent .teacherNew').css('display', 'none');
        // $('.sideContent .numberSetting').css('display', 'none');
        // $('.sideContent .recycle').css('display', 'none');
    }
    background();
    /**开始就展示 */
    $('.sideContent .tiaoshi').css('display', 'block');
    $(backgroundList[0]).css('background', "url('../../img/class.png') 20px center no-repeat").find('a').css('color', '#fcb636');






    /**展示不同button不同内容 */

    /**添加 */
    $('.tiaoshi .paddingLeft').find('input[value="添加"]').click(function () {
        // $('.modal_content').html('<div class="add"><div class="classNew"><p>课程基本信息</p><ul><li><span>Date</span><input type="text" ></li><li><span>Course</span><input type="text" ></li><li><span>Hours</span><input type="text" ></li><li><span>Employee  Name</span><input type="text" ></li><li><span>Employee  #</span><input type="text" ></li></ul></div><div class="studentList"><p>学生列表</p><ul><li class="teshu"><input type="checkbox"><span class="listFirst">Name</span><span>LN</span><span>FN</span></li><li><img src="../../img/add01.png" alt="" class="addImg"><img src="../../img/jian01.png" alt="" class="delImg"><input type="checkbox"><input type="text"><input type="text"><input type="text"></li></ul><div class="addstudent"><input class="addStudent" type="button"  value="+&nbsp;添加学生"></div><div class="addSave"><input type="button"  value="取消"><input type="button"  value="提交"></div></div></div>')
        $('#addmodal .modal_content').find('.add input[value="取消"]').click(function (event) {
            addHide()
            event.stopPropagation();
        });
        /**上课信息的添加显示弹框 */
        $('.modal_content').find('.add .addStudent').click(function (event) {

            $('#Topcover').css('display', 'block')
            $('#Topmodal').css('display', 'block')
        })

        /**点击加减号添加删除 */
        $('.modal_content').on('click', '.addImg', function (event) {
            event.stopPropagation()
            $('.modal_content').find('.add .studentList ul').find('li').last().after('<li><img src="../../img/add01.png" alt="" class="addImg"><img src="../../img/jian01.png" alt="" class="delImg"><input type="checkbox"><input type="text"><input type="text"><input type="text"></li>')

        })
        $('.modal_content').on('click', '.delImg', function (event) {
            event.stopPropagation()
            $(this).parent('li').remove()


        })

    })
    $('.studentBig .paddingLeft').find('input[value="添加"]').click(function () {
        // $('.modal_content').html('<div class="addList"><p>添加学生信息</p><ul><li><span>Name&nbsp;:</span><input type="text" value=""></li><li><span>LN&nbsp;:</span><input type="text" value=""></li><li><span>FN&nbsp;:</span><input type="text" value=""></li></ul><div class="addListButton"><input type="button" value="取消"><input type="button" value="添加"></div></div>')
        $('.modal_content').find('.addList input[value="取消"]').click(function (event) {
            event.stopPropagation();
            studentaddHide();
        })
    })

    $('.teacherNew .paddingLeft').find('input[value="添加"]').click(function () {
        // $('.modal_content').html('<div class="teacherAddList"><p>添加教师信息</p><ul><li><span>Name&nbsp;:</span><input type="text" value=""></li><li><span>LN&nbsp;:</span><input type="text" value=""></li><li><span>FN&nbsp;:</span><input type="text" value=""></li><li><span>Employee #&nbsp;:</span><input type="text" value=""></li></ul><div class="addListButton"><input type="button" value="取消"><input type="button" value="添加"></div></div>')
        $('.modal_content').find('.teacherAddList input[value="取消"]').click(function (event) {
            event.stopPropagation();
            teacheraddHide()
        })
    })


    /**导入 */
    // $('.tiaoshi .paddingLeft').find('input[value="导入"]').click(function () {
    //     $('.modal_content').text("2")
    // })
    // $('.studentBig .paddingLeft').find('input[value="导入"]').click(function () {
    //     $('.modal_content').html('')

    // })
    // $('.teacherNew .paddingLeft').find('input[value="导入"]').click(function () {
    //     $('.modal_content').html('')

    // })

    /**导出 */
    $('.tiaoshi .paddingLeft').find('input[value="导出"]').click(function () {
        // $('.modal_content').html('')
        $('#modal .modal_content').find('.modal_button input[value="取消"]').click(function (event) {
            event.stopPropagation();
            showHide();
        });
    })
    $('.studentBig .paddingLeft').find('input[value="导出"]').click(function () {
        // $('.modal_content').html('<div class="daochu"><p>请选择需要导出的Excel字段</p><div class="checkAll"><input type="checkbox" ><span>全选</span></div><ul><li><input type="checkbox" ><span>Course</span></li><li><input type="checkbox" ><span>Date</span></li><li><input type="checkbox" ><span>Name</span></li><li><input type="checkbox" ><span>LN</span></li><li><input type="checkbox" ><span>FN</span></li><li><input type="checkbox" ><span>Hours</span></li><li><input type="checkbox" ><span>Time</span></li><li><input type="checkbox" ><span>Employee #</span></li><li><input type="checkbox" ><span>Employee Name</span></li></ul><div class="modal_button"><input type="button"  value="取消" class="delete"><input type="button"  value="确定"></div></div>')
        $('#studentmodal .modal_content').find('.modal_button input[value="取消"]').click(function (event) {
            event.stopPropagation();
            studentHide()
        })
    })
    $('.teacherNew .paddingLeft').find('input[value="导出"]').click(function () {
        // $('.modal_content').html('<div class="daochu"><p>请选择需要导出的Excel字段</p><div class="checkAll"><input type="checkbox" ><span>全选</span></div><ul><li><input type="checkbox" ><span>Course</span></li><li><input type="checkbox" ><span>Date</span></li><li><input type="checkbox" ><span>Name</span></li><li><input type="checkbox" ><span>LN</span></li><li><input type="checkbox" ><span>FN</span></li><li><input type="checkbox" ><span>Hours</span></li><li><input type="checkbox" ><span>Time</span></li><li><input type="checkbox" ><span>Employee #</span></li><li><input type="checkbox" ><span>Employee Name</span></li></ul><div class="modal_button"><input type="button"  value="取消" class="delete"><input type="button"  value="确定"></div></div>')
        $('#teachermodal .modal_content').find('.modal_button input[value="取消"]').click(function (event) {
            event.stopPropagation();
            teacherHide();
        })
    })


    /**编辑  */
    // $('#editmodal .modal_content').find('.editButton input[value="取消"]').click(function (event) {
    //     event.stopPropagation();
    //     editHide();
    // })
    // $('#editstudentmodal .modal_content').find('.editButton input[value="取消"]').click(function (event) {
    //     event.stopPropagation();
    //     editstudentHide();
    // })
    // $('#teachereditmodal .modal_content').find('.editButton input[value="取消"]').click(function (event) {
    //     event.stopPropagation();
    //     editteacherHide();
    // })


    /**删除 */
    var deleteChecked = $('.tiaoshi .mainShow').find('ul li')
    var studentDelete = $('.studentContentMain').find('ul li')
    var teacherDelete = $('.teacherNew .mainShow').find('ul li')

    function del(a) {
        for (var i = 0; i < a.length; i++) {
            if ($(a[i]).find('input[type="checkbox"]').is(':checked') == true) {
                $(a[i]).remove()
            }
        }
    }
    $('.tiaoshi .paddingLeft').find('input[value="删除"]').click(function () {
        // showHide();
        del(deleteChecked);
    })

    $('.studentBig .paddingLeft').find('input[value="删除"]').click(function () {
        // showHide();
        del(studentDelete);
    })

    $('.teacherNew .paddingLeft').find('input[value="删除"]').click(function () {
        // showHide();
        del(teacherDelete);
    })


    /**回收站的还原与删除弹框 */
    $('.recycle .operate').find('.comeback').click(function () {

        $('.smallModal_content').html('<p style=" margin-top: 60px;text-align: center;font-size: 20px;">确定还原所选文件?</p><div style=" margin-top: 50px;text-align: center;"><input type="button" value="取消"><input type="button" value="确定" style="background: skyblue;"></div>')
        $('.smallModal_content').find('input').css('width', 100).css('height', 40).css('border-radius', 10).css('border', 'none').css('margin', '0 15px 0 15px')
        $('.smallModal_content').find('input[value="取消"]').click(function (event) {
            event.stopPropagation();
            smallshowHide();
        })
    })
    $('.recycle .re_button').find('input[value="还原"]').click(function () {

        $('.smallModal_content').html('<p style=" margin-top: 60px;text-align: center;font-size: 20px;">确定还原所选文件?</p><div style=" margin-top: 50px;text-align: center;"><input type="button" value="取消"><input type="button" value="确定" style="background: skyblue;"></div>')
        $('.smallModal_content').find('input').css('width', 100).css('height', 40).css('border-radius', 10).css('border', 'none').css('margin', '0 15px 0 15px')
        $('.smallModal_content').find('input[value="取消"]').click(function (event) {
            event.stopPropagation();
            smallshowHide();
        })
    })

    $('.recycle .operate').find('.delete').click(function () {
        $('.smallModal_content').html('<p style=" margin-top: 60px;text-align: center;font-size: 20px;">文件删除后无法恢复，是否确定删除所选文件？</p><div style=" margin-top: 50px;text-align: center;"><input type="button" value="取消"><input type="button" value="确定" style="background: skyblue;"></div>')
        $('.smallModal_content').find('input').css('width', 100).css('height', 40).css('border-radius', 10).css('border', 'none').css('margin', '0 15px 0 15px')
        $('.smallModal_content').find('input').click(function (event) {
            if ($(this).val() == "取消") {
                event.stopPropagation();
                smallshowHide();
            } else {

                smallshowHide();
            }

        })
    })
    $('.recycle .re_button').find('input[value="删除"]').click(function () {
        $('.smallModal_content').html('<p style=" margin-top: 60px;text-align: center;font-size: 20px;">文件删除后无法恢复，是否确定删除所选文件？</p><div style=" margin-top: 50px;text-align: center;"><input type="button" value="取消"><input type="button" value="确定" style="background: skyblue;"></div>')
        $('.smallModal_content').find('input').css('width', 100).css('height', 40).css('border-radius', 10).css('border', 'none').css('margin', '0 15px 0 15px')
        $('.smallModal_content').find('input').click(function (event) {
            if ($(this).val() == "取消") {
                event.stopPropagation();
                smallshowHide();
            } else {

                smallshowHide();
            }

        })
    })
    /**上课信息编辑 */
    $('.sideContent .tiaoshi .classEdit').find('input[value="取消"]').click(function () {
        $('.tiaoshi .contentHead').css('display', 'block');
        $('.tiaoshi .mainContent').css('display', 'block')
        $('.tiaoshi .classEdit').css('display', 'none')
    })
    $('.sideContent .tiaoshi .editAll').click(function () {
        $('.tiaoshi .contentHead').css('display', 'block');
        $('.tiaoshi .mainContent').css('display', 'block')
        $('.tiaoshi .classEdit').css('display', 'none')
    })
    /**学生信息编辑 */
    $('.sideContent .studentBig .studentEdit').find('input[value="取消"]').click(function () {
        $('.studentBig .contentHead').css('display', 'block');
        $('.studentBig .studentContent').css('display', 'block')
        $('.studentBig .studentEdit').css('display', 'none')
    })
    $('.sideContent .studentBig .studentEdit .editAll').click(function () {
        $('.studentBig .contentHead').css('display', 'block');
        $('.studentBig .studentContent').css('display', 'block')
        $('.studentBig .studentEdit').css('display', 'none')
    })
    /**学生信息添加 */
    $('.sideContent .studentBig .addList').find('input[value="取消"]').click(function () {
        $('.studentBig .contentHead').css('display', 'block');
        $('.studentBig .studentContent').css('display', 'block')
        $('.studentBig .addList').css('display', 'none')
    })
    $('.sideContent .studentBig .addList .editAll').click(function () {
        $('.studentBig .contentHead').css('display', 'block');
        $('.studentBig .studentContent').css('display', 'block')
        $('.studentBig .addList').css('display', 'none')
    })

    /**教师信息编辑 */
    $('.sideContent .teacherNew .teacherEdit').find('input[value="取消"]').click(function () {
        $('.teacherNew .contentHead').css('display', 'block');
        $('.teacherNew .mainContent').css('display', 'block')
        $('.teacherNew .teacherEdit').css('display', 'none')
    })
    $('.sideContent .teacherNew .teacherEdit .editAll').click(function () {
        $('.teacherNew .contentHead').css('display', 'block');
        $('.teacherNew .mainContent').css('display', 'block')
        $('.teacherNew .teacherEdit').css('display', 'none')
    })

    /**教师信息添加 */
    $('.sideContent .teacherNew .addList').find('input[value="取消"]').click(function () {
        $('.teacherNew .contentHead').css('display', 'block');
        $('.teacherNew .mainContent').css('display', 'block')
        $('.teacherNew .addList').css('display', 'none')
    })
    $('.sideContent .teacherNew .addList .editAll').click(function () {
        $('.teacherNew .contentHead').css('display', 'block');
        $('.teacherNew .mainContent').css('display', 'block')
        $('.teacherNew .addList').css('display', 'none')
    })


    /**学生个人信息详情 */
    var studentDetail = $('.studentContent .studentContentMain ul li')
    for (var i = 0; i < studentDetail.length; i++) {
        //    console.log(studentDetail[i])
        $(studentDetail[i]).click(function () {
            // //  console.log(123)
            // $('.studentBig .contentHead').css('display', 'none');
            // $('.studentBig .studentContent').css('display', 'none')
            // $('.studentBig .studentDetail').css('display', 'block')
        })
    }
    /**点击图片返回 */
    $('.studentDetail .editAll').click(function () {
        location.href = ""
    })
    $('.studentDetail .return').click(function () {
        location.href = ""
        // $('.studentBig .contentHead').css('display', 'block');
        // $('.studentBig .studentContent').css('display', 'block')
        // $('.studentBig .studentDetail').css('display', 'none')

    })

    /**tab栏 */
    var tab = $('.studentDetail .stuedentDetailContent .Nav li')
    for (var k = 0; k < tab.length; k++) {
        $(tab[0]).addClass('active')
        $('.studentDetail .stuedentDetailContent .history').css('display', 'none');
        $(tab[0]).click(function () {
            $(this).addClass('active').siblings().removeClass('active')
            $('.studentDetail .stuedentDetailContent .new').css('display', 'block');
            $('.studentDetail .stuedentDetailContent .history').css('display', 'none');
        })
        $(tab[1]).click(function () {
            $(this).addClass('active').siblings().removeClass('active')
            $('.studentDetail .stuedentDetailContent .new').css('display', 'none');
            $('.studentDetail .stuedentDetailContent .history').css('display', 'block');
        })
    }


    /**教师个人详情 */
    var studentDetail = $('.teacherNew .mainContent .mainShow ul li')
    for (var i = 0; i < studentDetail.length; i++) {
        //    console.log(studentDetail[i])
        $(studentDetail[i]).click(function () {
            //  console.log(123)

            // $('.teacherNew .contentHead').css('display', 'none');
            // $('.teacherNew .mainContent').css('display', 'none')
            // $('.teacherNew .teacherDetail').css('display', 'block')
        })
    }
    /**点击图片返回 */
    $('.teacherDetail .return').click(function () {})
    $('.teacherDetail .return').click(function () {
        location.href = ""
        // $('.teacherNew .contentHead').css('display', 'block');
        // $('.teacherNew .mainContent').css('display', 'block')
        // $('.teacherNew .teacherDetail').css('display', 'none')
    })

    /**tab栏 */
    var tab = $('.teacherDetail .teacherDetailContent .Nav li')
    for (var k = 0; k < tab.length; k++) {
        $(tab[0]).addClass('active')
        $('.teacherDetail .teacherDetailContent .history').css('display', 'none');
        $(tab[0]).click(function () {
            $(this).addClass('active').siblings().removeClass('active')
            $('.teacherDetail .teacherDetailContent .new').css('display', 'block');
            $('.teacherDetail .teacherDetailContent .history').css('display', 'none');
        })
        $(tab[1]).click(function () {
            $(this).addClass('active').siblings().removeClass('active')
            $('.teacherDetail .teacherDetailContent .new').css('display', 'none');
            $('.teacherDetail .teacherDetailContent .history').css('display', 'block');
        })
    }

    /**所有checkedbox的全选与反选 */
    // var checkALL = $('.all')
    // var coverList=$('.cover')
// function trans(element){
//     for (var i = 0; i < element.length; i++) {
//         $(element[i]).click(function (e) {
//             if ($(this).is(':checked') == true) {
//                 $(":checkbox").attr("checked", "checked").prop('checked', true);
//             } else {
//                 $(":checkbox").attr("checked", "checked").prop('checked', false);
//             }
//             e.stopPropagation()
//         });

//     }
// }
// trans(checkALL);
// trans(coverList);
/**上课信息的添加checkbox*/
$('#addmodal .studentList .teshu input[type="checkbox"]').click(function (e) {
    if ($(this).is(':checked') == true) {
        $(this).parent('li').siblings().find('input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(this).parent('li').siblings().find('input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
});
$('.registrationAddInfomation .listFirst .all').click(function (e) {
    if ($(this).is(':checked') == true) {
        $(this).parent('.listFirst').siblings().find('input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(this).parent('.listFirst').siblings().find('input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
});

$('.baseContent .mainShowTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        $(".baseContent").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".baseContent").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
});
/**上课信息的添加学生按钮 */
$('#Topmodal .contentTitle input[type="checkbox"]').click(function (e) {
    if ($(this).is(':checked') == true) {
        $('#Topmodal .mainShow').find('input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $('#Topmodal .mainShow').find('input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
});


/**报名信息的添加checkbox */
$('.cover').click(function (e) {
    if ($(this).is(':checked') == true) {
        $('#baseStudentmodal .mainShow input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $('#baseStudentmodal .mainShow input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
});
$('.registrationAddInfomation .listFirst .all').click(function (e) {
    if ($(this).is(':checked') == true) {
        $(this).parent('.listFirst').siblings().find('input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(this).parent('.listFirst').siblings().find('input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
});

$('.baseContent .mainShowTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        $(".baseContent").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".baseContent").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
});

/**上课信息 */
$('.tiaoshi .contentTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        $(".tiaoshi").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".tiaoshi").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
})
/**学生信息 */
$('.studentBig .studentContentTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        console.log(123)
        $(".studentBig").find('.studentContentMain ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".studentBig").find('.studentContentMain ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
})
/**老师信息 */
$('.teacherNew .contentTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        console.log(123)
        $(".teacherNew").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".teacherNew").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
})
/**回收站 */
$('.recycle .recycleContentTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        console.log(123)
        $(".recycle").find('.recycleMain ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".recycle").find('.recycleMain ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
})
/**学生信息详情 */
$('.studentDetail .detailContent .applyTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        $(".studentDetail").find('.detailContent .applyTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".studentDetail").find('.detailContent .applyTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
})
$('.studentDetail .detailContent .classTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        $(".studentDetail").find('.detailContent .classTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".studentDetail").find('.detailContent .classTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
})

/**教师信息详情 */

$('.teacherDetail .detailContent .applyTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        $(".teacherDetail").find('.detailContent .applyTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".teacherDetail").find('.detailContent .applyTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
})
$('.teacherDetail .detailContent .classTitle .all').click(function(e){
    if ($(this).is(':checked') == true) {
        $(".teacherDetail").find('.detailContent .classTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    } else {
        $(".teacherDetail").find('.detailContent .classTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    }
    e.stopPropagation()
})


  




    // var check = $('input[name="hxy"]');
    // for(var i=0;i<check.length;i++){
    //     console.log(check[i])
    // }


    /**回收站的tab切换 */
    var recycleList = $('.recycle .recycleTitle ul li')
    var recycleContent = $('.recycle .recycleContent')
    $(recycleList[0]).click(function () {
        $(recycleContent[0]).css('display', 'block')
        $(recycleContent[1]).css('display', 'none')
        $(recycleContent[2]).css('display', 'none')
        $(recycleContent[3]).css('display', 'none')
    })
    $(recycleList[1]).click(function () {
        $(recycleContent[1]).css('display', 'block')
        $(recycleContent[0]).css('display', 'none')
        $(recycleContent[2]).css('display', 'none')
        $(recycleContent[3]).css('display', 'none')
    })
    $(recycleList[2]).click(function () {
        $(recycleContent[2]).css('display', 'block')
        $(recycleContent[0]).css('display', 'none')
        $(recycleContent[1]).css('display', 'none')
        $(recycleContent[3]).css('display', 'none')
    })
    $(recycleList[3]).click(function () {
        $(recycleContent[3]).css('display', 'block')
        $(recycleContent[0]).css('display', 'none')
        $(recycleContent[1]).css('display', 'none')
        $(recycleContent[2]).css('display', 'none')
    })


    /**阻止点击冒泡 */
    $("input[name='hxy']").click(function (e) {
        e.stopPropagation()
    })


    /**悬浮编辑 */
    $('.tiaoshi ').find('.mainShow .edit').click(function () {
        console.log(123)
        $('.tiaoshi .contentHead').css('display', 'none');
        $('.tiaoshi .mainContent').css('display', 'none')
        $('.tiaoshi .classEdit').css('display', 'block')
    })
    $('.studentBig').find('.studentContent .edit').click(function (e) {
        // $('#edistudentcover').show()
        // $('#editstudentmodal').show()

        $('.studentBig .contentHead').css('display', 'none');
        $('.studentBig .studentContent').css('display', 'none')
        $('.studentBig .studentEdit').css('display', 'block')
        e.stopPropagation()
    })


    $('.teacherNew').find('.mainShow .edit').click(function (e) {
        // $('#teachereditcover').show()
        // $('#teachereditmodal').show()
        $('.teacherNew .contentHead').css('display', 'none');
        $('.teacherNew .mainContent').css('display', 'none')
        $('.teacherNew .teacherEdit').css('display', 'block')
        e.stopPropagation()
    })


    /**人员设置 */
    $('.settingNumber .settingTitle').find('input[value="添加"]').click(function () {
        // $('#settingcover').show();
        // $('#settingmodal').show()
        // $('#settingmodal .settingmodal_content').html('<p class="add">添加人员</p><div class="compire"><ul><li><span>登录名</span><input type="text" placeholder="&nbsp;(用户名只能由2-15个英文字母或数字组成。如michael88)"></li><li><span>密码</span><input type="password" placeholder="&nbsp;(请输入密码)"></li><li><span>确认密码</span><input type="text" placeholder="&nbsp;(请再次输入密码)"></li><li><span>姓名</span><input type="text" placeholder="&nbsp;(请输入真实姓名)"></li></ul></div><div class="userCompire"><p>下次登录必须修改密码</p><p class="gray">强制用户下次登录时必须修改密码</p><ul><li><input type="checkbox" ><span>是</span></li><li><input type="checkbox" ><span>否</span></li></ul><div class="userButton"><input type="button" value="取消"><input type="button" value="添加"></div></div>')
        location.href = "./settingAdd.html";
    });
    $('.settingNumber .settingTitle').find('input[value="编辑"]').click(function () {
        location.href = "./settingEdit.html";
        // $('#settingcover').show();
        // $('#settingmodal').show()
        // $('#settingmodal .settingmodal_content').html('<p class="add">编辑人员</p><div class="compire"><ul><li><span>登录名</span><input type="text" placeholder="&nbsp;(用户名只能由2-15个英文字母或数字组成。如michael88)"></li><li><span>密码</span><input type="password" placeholder="&nbsp;(请输入密码)"></li><li><span>确认密码</span><input type="text" placeholder="&nbsp;(请再次输入密码)"></li><li><span>姓名</span><input type="text" placeholder="&nbsp;(请输入真实姓名)"></li></ul></div><div class="userCompire"><p>下次登录必须修改密码</p><p class="gray">强制用户下次登录时必须修改密码</p><ul><li><input type="checkbox" ><span>是</span></li><li><input type="checkbox" ><span>否</span></li></ul><div class="userButton"><input type="button" value="取消"><input type="button" value="保存"></div></div>')
        // $('#settingmodal .settingmodal_content').find('input[value="取消"]').click(function () {
        //     $('#settingcover').hide();
        //     $('#settingmodal').hide()
        // })
    });
    $('.settingNumber .settingTitle').find('input[value="禁用"]').click(function () {
        $('#smallSettingcover').show();
        $('#smallSettingmodal').show();
        var checkList = $('.settingContent li input[type="checkbox"]');
        var arr = [];
        for (var i = 0; i < checkList.length; i++) {
            if ($(checkList[i]).is(':checked') == true) {
                arr.push(checkList[i]);
                if (arr.length >= 2) {
                    $('#smallSettingmodal .smallSettingModal_content').html('<p>是否禁用您勾选的所有帐号</p><div class="smallSettingButton"><input type="button" value="否"><input type="button" value="是"></div>')
                };
                if (arr.length < 2) {
                    $('#smallSettingmodal .smallSettingModal_content').html('<p>是否禁用"liuxinlun"这个帐号</p><div class="smallSettingButton"><input type="button" value="否"><input type="button" value="是"></div>')
                };
            };
        };


        $('#smallSettingmodal .smallSettingModal_content').find('input[value="否"]').click(function () {
            $('#smallSettingcover').hide();
            $('#smallSettingmodal').hide();
        });
    });
    $('.settingNumber .settingTitle').find('input[value="删除"]').click(function () {
        $('#smallSettingcover').show();
        $('#smallSettingmodal').show();
        var arr1 = [];
        var allList = $('.settingContent li input[type="checkbox"]');
        for (var i = 0; i < allList.length; i++) {
            if ($(allList[i]).is(':checked') == true) {
                arr1.push(allList[i]);
                if (arr1.length >= 2) {
                    $('#smallSettingmodal .smallSettingModal_content').html('<p>是否删除您勾选的所有帐号</p><div class="smallSettingButton"><input type="button" value="否"><input type="button" value="是"></div>')
                };
                if (arr1.length < 2) {
                    $('#smallSettingmodal .smallSettingModal_content').html('<p>是否删除"liuxinlun"这个帐号</p><div class="smallSettingButton"><input type="button" value="否"><input type="button" value="是"></div>')
                };
            };
        };

        $('#smallSettingmodal .smallSettingModal_content').find('input[value="否"]').click(function () {
            $('#smallSettingcover').hide();
            $('#smallSettingmodal').hide();
        });
    });

    $("#settingmodal #settingclose").click(function () {
        $('#settingcover').hide();
        $('#settingmodal').hide();
    });
    $("#smallSettingmodal #smallSettingclose").click(function () {
        $('#smallSettingcover').hide();
        $('#smallSettingmodal').hide();
    });
    $('.allChecked').click(function () {

        if ($(this).is(':checked') == true) {
            $(":checkbox").attr("checked", "checked").prop('checked', true);
        } else {
            $(":checkbox").attr("checked", "checked").prop('checked', false);
        };
    });


    $('.editNumber .edit .editAll').click(function () {
        location.href = "./setting.html";
    })
    $('.addNumber .add .editAll').click(function () {
        location.href = "./setting.html";
    })


    /**点击取消 */
    $('.editNumber input[value="取消"]').click(function () {
        location.href = "./setting.html";;
    });
    $('.addNumber input[value="取消"]').click(function () {
        location.href = "./setting.html";
    });







    /**报名信息 */
    /**金额的计算 */
    var discount = $('.discount');
    var receivable = $('.receivable');
    var receipts = $('.receipts');
    $('.discount').bind('input propertychange', function () {
        receipts.val(receivable.val() - discount.val())
    });
    $('.receivable').bind('input propertychange', function () {
        receipts.val(receivable.val() - discount.val())
    });

    /**点击添加课件类型按钮 */
    $('.information .addClass input[type="button"]').click(function () {
        $('.addClass').before($('.registrationAddInfomation .information .display').last().clone(true).css("margin-top", 20).css('display', 'block'))
    })

    $('.editInformation .addClass input[type="button"]').click(function () {
        $('.addClass').before($('.regidtrationEdit .editInformation .display').last().clone(true).css("margin-top", 20).css('display', 'block'))
    })

    /** 点击加减号添加删除*/
    $('.registrationAddInfomation .add').click(function () {
        $('.registrationAddInfomation .stdentList ul').append($(".stdentList .listThirt").last().clone(true).css('display', 'block'))
    })
    $('.registrationAddInfomation .delete').click(function () {
        $(this).parent('.listThirt').remove();
    })


    /**基础设置 */
    // nav收缩展开
    $('.navMenu li a').on('click', function () {
        var parent = $(this).parent().parent(); //获取当前页签的父级的父级
        var labeul = $(this).parent("li").find(">ul")
        if ($(this).parent().hasClass('open') == false) {
            //展开未展开
            parent.find('ul').slideUp(300);
            parent.find("li").removeClass("open")
            parent.find('li a').removeClass("active").find(".arrow").removeClass("open")
            $(this).parent("li").addClass("open").find(labeul).slideDown(300);
            $(this).addClass("active").find(".arrow").addClass("open")
        } else {
            $(this).parent("li").removeClass("open").find(labeul).slideUp(300);
            if ($(this).parent().find("ul").length > 0) {
                $(this).removeClass("active").find(".arrow").removeClass("open")
            } else {
                $(this).addClass("active")
            }
        }

    });
     //基础设置遮罩层

     /**添加课程 */
     $('.addClass').click(function(){
         $('#basecover').show();
         $('#basemodal').show();
     })

     $('#baseclose').click(function(){
        $('#basecover').hide();
        $('#basemodal').hide();
     })
     $('#basemodal .modal_content .Button input[value="取消"]').click(function(){
        $('#basecover').hide();
        $('#basemodal').hide();
     })

     /**添加类型 */
     $('.addKinds').click(function(){
         $('#kindscover').show()
         $('#kindsmodal').show();
     })
     $('#kindsclose').click(function(){
        $('#kindscover').hide();
        $('#kindsmodal').hide();
     })
     $('#kindsmodal .modal_content .Button input[value="取消"]').click(function(){
        $('#kindscover').hide();
        $('#kindsmodal').hide();
     })

     /**报名信息的学生添加 */
     $('.registrationAddInfomation .addButton').click(function(){
        $('#baseStudentcover').show()
        $('#baseStudentmodal').show();
     })
     $('#baseStudentclose').click(function(){
        $('#baseStudentcover').hide();
        $('#baseStudentmodal').hide();
     })



     /**学生信息详情的改动 */
        $('.studentDetail .detailContent .applyTitle .showOrHide').click(function(){
            $('.studentDetail .detailContent .applyTitle ul').toggle(500)
            $('.studentDetail .detailContent .applyTitle .showOrHide').toggle()
            
        })
        $('.studentDetail .detailContent .classTitle .showOrHide').click(function(){
            $('.studentDetail .detailContent .classTitle ul').toggle(500)
            $('.studentDetail .detailContent .classTitle .showOrHide').toggle()
        })

        /**教师信息详情的改动 */
        $('.teacherDetail .detailContent .applyTitle .showOrHide').click(function(){
            $('.teacherDetail .detailContent .applyTitle ul').toggle(500)
            $('.teacherDetail .detailContent .applyTitle .showOrHide').toggle()
            
        })
        $('.teacherDetail .detailContent .classTitle .showOrHide').click(function(){
            $('.teacherDetail .detailContent .classTitle ul').toggle(500)
            $('.teacherDetail .detailContent .classTitle .showOrHide').toggle()
        })
})