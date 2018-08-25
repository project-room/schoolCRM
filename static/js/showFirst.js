$(function () {
    /**日期显示 */
    laydate.render({
        elem: '#dateStart',
        theme: '#fcb636',
        format: 'yyyy-MM-dd'
    });
    laydate.render({
        elem: '#dateEnd',
        theme: '#fcb636',
        format: 'yyyy-MM-dd'
    });

    laydate.render({
        elem: '#dateLeft',
        theme: '#fcb636',
        format: 'yyyy-MM-dd'
    });

    laydate.render({
        elem: '#dateRight',
        theme: '#fcb636',
        format: 'yyyy-MM-dd'
    });
    laydate.render({
        elem: '#moneyDate',
        theme: '#fcb636',
        format: 'yyyy-MM-dd'
    });
      laydate.render({
        elem: '#money',
        theme: '#fcb636',
        format: 'yyyy-MM-dd'
    });

    /** 基础设置的里侧导航栏胡显示隐藏*/
    $('.navShow').click(function () {
        $('.baseLeftSide').toggle()
        if($('.baseLeftSide').css('display')=='block'){
             $('.baseSettingInformation').css('left',181)
           $('.baseContent').width($('.baseSettingInformation').width() - 210);
             $('.changes').css('visibility','hidden')
        }else{
            $('.baseSettingInformation').css('left',0)
            $('.baseContent').width($('.baseSettingInformation').width()-30);
            $('.changes').css('visibility','inherit')
        }
    })


    /**教师信息里的密码修改 */

    $('.numberSetting .correct').click(function (event) {
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
    $('.addNumber').width($('body').width() - 200);
    $('.editNumber').width($('body').width() - 200);
    $('.registrationInformation').width($('body').width() - 200);
    $('.regidtrationEdit').width($('body').width() - 200);

    $('.classrecycleContent,.studentrecycleContent,.teacherrecycleContent,.peoplerecycleContent,.recycleLIst').width($('body').width() - 200);
    $('.baseSettingInformation').width($('body').width() - 200);
    $('.baseContent').width($('.baseSettingInformation').width() - 210);
    $('.studentDetail .content').width($('.studentDetail').width() + 100);
    $('.teacherDetail .content').width($('.teacherDetail').width() + 100);




    $('#basecover').height($('body').height())
    $('.content').height($('.sideContent').height() - 190)


    $('.baseLeftSide').height($('body').height() - 62)


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
        $('#smallcover').hide();
        $("#smallmodal").hide();
    }

    function studentHide() {
        $('#studentmodal').hide();
        $('#studentcover').hide();
    }

    function teacherHide() {
        $('#teachermodal').hide();
        $('#teachercover').hide();
    }

    function addHide() {
        $('#addcover').hide();
        $('#addmodal').hide();
    }

    function studentaddHide() {
        $('#studentaddcover').hide();
        $('#studentaddmodal').hide();
    }

    function teacheraddHide() {
        $('#teacheraddcover').hide();
        $('#teacheraddmodal').hide();
    }

    function editHide() {
        $('#editcover').hide();
        $('#editmodal').hide();
    }

    function editstudentHide() {
        $('#edistudentcover').hide();
        $('#editstudentmodal').hide();
    }

    function editteacherHide() {
        $('#teachereditcover').hide();
        $('#teachereditmodal').hide();
    }
    function restritration() {
         $('#registercover').hide();
        $('#registermodal').hide();
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
    restritration();
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
;
    $("#addclose").click(function () {
        addHide();
    })
    $('#studentaddclose').click(function () {
        studentaddHide()
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
        $('#teacheraddclose').click(function () {
          $('#teacheraddcover').hide()
    $('#teacheraddmodal').hide()
})

    $('#study_export_btn').click(function () {
        showHide()
    })
     $('#student_export_btn').click(function () {
        studentHide()
    })
     $('#teacher_export_btn').click(function () {
        teacherHide()
    })


    $('#registerclose').click(function () {
        restritration()
    })


    /**顶层弹框的关闭 */
    $('#Topmodal #Topclose').click(function () {
        $('#Topcover').css('display', 'none');
        $('#Topmodal').css('display', 'none')
        $('#Topmodal .TopModal_content input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    })



    //显示弹框遮罩
    var tiaoshi = $(".tiaoshi .paddingLeft");
    var studentBig = $('.studentBig .paddingLeft');
    var teacherBig = $('.teacherNew .paddingLeft');


    /**添加 */
    tiaoshi.find('input[value="添加"]').click(function () {
        $('#addcover').show()
        $("#addmodal").show()
    })
    studentBig.find('input[value="添加"]').click(function () {
        $('#studentaddcover').show()
        $('#studentaddmodal').show()
    })
    teacherBig.find('input[value="添加"]').click(function () {
        $('#teacheraddcover').show()
        $('#teacheraddmodal').show()
    })

    /**编辑 */
    tiaoshi.find('input[value="编辑"]').click(function () {
        $('#editcover').show()
        $("#editmodal").show()
    })
    studentBig.find('input[value="编辑"]').click(function () {
        $('#edistudentcover').show()
        $("#editstudentmodal").show()
    })

    teacherBig.find('input[value="编辑"]').click(function () {
        $('#teachereditcover').show();
        $('#teachereditmodal').show();
    })
    teacherBig.find('input[value="添加"]').click(function () {
        $('#teacheraddcover').show();
        $("#teacheraddmodal").show();
    })



$('.studentContentMain .operate').find('.edit').click(function () {
         $('#edistudentcover').show()
        $("#editstudentmodal").show()
})
    $('.teacherNew .operate .edit').click(function () {
        $('#teachereditcover').show();
        $('#teachereditmodal').show();
})

  $('.tiaoshi .operate .edit').click(function () {
        $('#editcover').show()
        $("#editmodal").show()
})


    /**展示左边导航的背景图 */
    var backgroundList = $('.leftSide .sideNav ul li')
    var arr = ['base01.png', 'registration01.png', 'class01.png', 'student01.png', 'teacher01.png',"operate01.png",'people01.png','accounts01.png','huishou01.png']
    function getResult(a, b) {
        if (a.length === b.length) {
            for (var i = 0; i < a.length; i++) {
                a[i].style.background = "url('/static/img/" + b[i] + "') 20px center no-repeat";
            }
        }
    }
    getResult(backgroundList, arr);

       var backgroundList = $('.leftSide .sideNav ul li')
    var arr = ['base01.png', 'registration01.png', 'class01.png', 'student01.png', 'teacher01.png',"operate01.png",'accounts01.png','huishou01.png']
    function getResultTwo(a, b) {
        if (a.length === b.length) {
            for (var i = 0; i < a.length; i++) {
                a[i].style.background = "url('/static/img/" + b[i] + "') 20px center no-repeat";
            }
        }
    }
    getResultTwo(backgroundList, arr);





    /**展示不同button不同内容 */

    /**添加 */
    $('.tiaoshi .paddingLeft').find('input[value="添加"]').click(function () {
        $('#addmodal .modal_content').find('.add input[value="取消"]').click(function (event) {
            addHide()
            event.stopPropagation();
        });
        /**上课信息的添加显示弹框 */
        $('.modal_content').find('.add .addStudent').click(function () {

            $('#Topcover').css('display', 'block')
            $('#Topmodal').css('display', 'block')
        })

        /**点击加减号添加删除 */
        $('.modal_content').on('click', '.addImg', function (event) {
            event.stopPropagation()
            $('.modal_content').find('.add .studentList ul').find('li').last().after('<li><img src="../static/img/add01.png" alt="" class="addImg"><img src="../static/img/jian01.png" alt="" class="delImg"><input type="checkbox"><input type="text"><input type="text"><input type="text"></li>')

        })
        $('.modal_content').on('click', '.delImg', function (event) {
            event.stopPropagation()
            $(this).parent('li').remove()


        })

    })
    $('.studentBig .paddingLeft').find('input[value="添加"]').click(function () {
        $('.modal_content').find('.addList input[value="取消"]').click(function (event) {
            event.stopPropagation();
            studentaddHide();
        })
    })

    $('.teacherNew .paddingLeft').find('input[value="添加"]').click(function () {
        $('.modal_content').find('.teacherAddList input[value="取消"]').click(function (event) {
            event.stopPropagation();
            teacheraddHide()
        })
    })




    /**导出 */
    $('.tiaoshi .paddingLeft').find('input[value="导出"]').click(function () {
        $('#modal .modal_content').find('.modal_button input[value="取消"]').click(function (event) {
            event.stopPropagation();
            showHide();
        });
    })
    $('.studentBig .paddingLeft').find('input[value="导出"]').click(function () {
        $('#studentmodal .modal_content').find('.modal_button input[value="取消"]').click(function (event) {
            event.stopPropagation();
            studentHide()
        })
    })
    $('.teacherNew .paddingLeft').find('input[value="导出"]').click(function () {
        $('#teachermodal .modal_content').find('.modal_button input[value="取消"]').click(function (event) {
            event.stopPropagation();
            teacherHide();
        })
    })


    /**编辑  */
    $('#editmodal .modal_content').find('.editButton input[value="取消"]').click(function (event) {
        event.stopPropagation();
        editHide();
    })
    $('#editstudentmodal .modal_content').find('.editButton input[value="取消"]').click(function (event) {
        event.stopPropagation();
        editstudentHide();
    })
    $('#teachereditmodal .modal_content').find('.editButton input[value="取消"]').click(function (event) {
        event.stopPropagation();
        editteacherHide();
    })


    /**删除 */
    var deleteChecked = $('.tiaoshi .mainShow').find('ul li')
    var studentDelete = $('.studentContentMain').find('ul li')
    var teacherDelete = $('.teacherNew .mainShow').find('ul li')

    function del(a) {
        for (var i = 0; i < a.length; i++) {
            if ($(a[i]).find('input[type="checkbox"]').is(':checked') == true) {
            }
        }
    }


    /**回收站的还原与删除弹框 */
    $('.recycle .operate').find('.comeback').click(function () {
        $('#recycle_cover').show();
        $("#recycle_modal").show()
    })

    $('.recycle .re_button').find('input[value="还原"]').click(function () {
         $('#recycle_cover').show();
         $("#recycle_modal").show()

    })
    $('#recycle_modal .smallModal_content').find('input[value="取消"]').click(function () {
        $('#recycle_cover').hide();
        $("#recycle_modal").hide()
    })
    $('#recycle_close').click(function(){
        $('#recycle_cover').hide();
        $("#recycle_modal").hide()
    })

    $('.recycle .operate').find('.delete').click(function () {
        $('#recycledeletecover').show();
        $("#recycledeletemodal").show()
    })
    $('.recycle .re_button').find('input[value="删除"]').click(function () {
        $('#recycledeletecover').show();
        $("#recycledeletemodal").show()
    })
    $('#recycledeletemodal .smallModal_content').find('input[value="取消"]').click(function () {
        $('#recycledeletecover').hide();
        $("#recycledeletemodal").hide()
    })
    $('#recycledeleteclose').click(function(){
        $('#recycledeletecover').hide();
        $("#recycledeletemodal").hide()
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


    /**教师信息编辑 */
    $('.sideContent .teacherNew .teacherEdit').find('input[value="取消"]').click(function () {
        $('.teacherNew .contentHead').css('display', 'block');
        $('.teacherNew .mainContent').css('display', 'block')
        $('.teacherNew .teacherEdit').css('display', 'none')
    })



    /**学生个人信息详情 */
    var studentDetail = $('.studentContent .studentContentMain ul li')



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

    $('.baseContent .mainShowTitle .all').click(function (e) {
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


    /**报名信息的添加checkbox*/
    $('.cover').click(function (e) {
        if ($(this).is(':checked') == true) {
            $('#baseStudentmodal .mainShow input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $('#baseStudentmodal .mainShow input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    });
    $('.re_all').click(function (e) {
           if ($(this).is(':checked') == true) {
            $('.register_detail').find('input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
           $('.register_detail').find('input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    })



    $('.registrationAddInfomation .listFirst .all').click(function (e) {
        if ($(this).is(':checked') == true) {
            $(this).parent('.listFirst').siblings().find('input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $(this).parent('.listFirst').siblings().find('input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    });
    /** 基础设置*/
    // $('.baseContent .mainShowTitle .all').click(function (e) {
    //     if ($(this).is(':checked') == true) {
    //         $(".baseContent").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
    //     } else {
    //         $(".baseContent").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    //     }
    //     e.stopPropagation();
    // });




    /**上课信息 */
    $('.tiaoshi .re_all').click(function (e) {
        if ($(this).is(':checked') == true) {
            $(".tiaoshi").find('.mainShow input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $(".tiaoshi").find('.mainShow input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    })
    /**学生信息 */
    $('.studentBig .studentContentTitle .all').click(function (e) {
        if ($(this).is(':checked') == true) {
            $(".studentBig").find('.studentContentMain ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $(".studentBig").find('.studentContentMain ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    });
    /**老师信息 */
    $('.teacherNew .contentTitle .all').click(function (e) {
        if ($(this).is(':checked') == true) {
            $(".teacherNew").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $(".teacherNew").find('.mainShow ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    })
    /**回收站 */
    $('.recycle .recycleContentTitle .all').click(function (e) {
        if ($(this).is(':checked') == true) {
            $(".recycle").find('.recycleMain ul input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $(".recycle").find('.recycleMain ul input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    })
    /**学生信息详情 */
    $('.studentDetail .detailContent .applyTitle .all').click(function (e) {
        if ($(this).is(':checked') == true) {
            $(".studentDetail").find('.detailContent .applyTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $(".studentDetail").find('.detailContent .applyTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    })
    $('.studentDetail .detailContent .classTitle .all').click(function (e) {
        if ($(this).is(':checked') == true) {
            $(".studentDetail").find('.detailContent .classTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $(".studentDetail").find('.detailContent .classTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    })

    /**教师信息详情 */

    $('.teacherDetail .detailContent .applyTitle .all').click(function (e) {
        if ($(this).is(':checked') == true) {
            $(".teacherDetail").find('.detailContent .applyTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $(".teacherDetail").find('.detailContent .applyTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    })
    $('.teacherDetail .detailContent .classTitle .all').click(function (e) {
        if ($(this).is(':checked') == true) {
            $(".teacherDetail").find('.detailContent .classTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', true);
        } else {
            $(".teacherDetail").find('.detailContent .classTitle input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
        }
        e.stopPropagation();
    })




    /**阻止点击冒泡 */
    $("input[name='hxy']").click(function (e) {
        e.stopPropagation()
    })


    /**悬浮编辑 */
    $('.tiaoshi ').find('.mainShow .edit').click(function () {
        $('.tiaoshi .classEdit').css('display', 'block')
    })
    $('.studentBig').find('.studentContent .edit').click(function (e) {

        $('.studentBig .contentHead').css('display', 'block');
        $('.studentBig .studentContent').css('display', 'block')
        e.stopPropagation()
    })


    $('.teacherNew').find('.mainShow .edit').click(function (e) {
        $('.teacherNew .contentHead').css('display', 'block');
        $('.teacherNew .mainContent').css('display', 'block')
        e.stopPropagation()
    })


    /**人员设置 */
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
        $('.registrationAddInfomation .addClass').before($('.registrationAddInfomation .information .display').last().clone(true).css("margin-top", 20).css('display', 'block'))
    })

    $('.editInformation .addClass input[type="button"]').click(function () {
        $('.editInformation .addClass').before($('.regidtrationEdit .editInformation .display').last().clone(true).css("margin-top", 20).css('display', 'block'))
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
    // $('.navMenu').on('click','li a',function () {
    //     var parent = $(this).parent().parent(); //获取当前页签的父级的父级
    //     var labeul = $(this).parent("li").find("ul")
    //     if ($(this).parent().hasClass('open') == false) {
    //         //展开未展开
    //         parent.find('ul').slideUp(300);
    //         parent.find("li").removeClass("open")
    //         parent.find('li a').removeClass("active").find(".arrow").removeClass("open")
    //         $(this).parent("li").addClass("open").find(labeul).slideDown(300);
    //         $(this).addClass("active").find(".arrow").addClass("open")
    //     } else {
    //         $(this).parent("li").removeClass("open").find(labeul).slideUp(300);
    //         if ($(this).parent().find("ul").length > 0) {
    //             $(this).removeClass("active").find(".arrow").removeClass("open")
    //         } else {
    //             $(this).addClass("active")
    //         }
    //     }
    // })




         // labeul.toggle(300)
    //基础设置遮罩层

    /**添加课程 */
    $('.addClass').click(function () {
        $('#basecover').show();
        $('#basemodal').show();
    })

    $('#baseclose').click(function () {
        $('#basecover').hide();
        $('#basemodal').hide();
    })
    $('#basemodal .modal_content .Button input[value="取消"]').click(function () {
        $('#basecover').hide();
        $('#basemodal').hide();
    })

    /**添加类型 */
    $('.addKinds').click(function () {
        $('#kindscover').show()
        $('#kindsmodal').show();
    })
    $('#kindsclose').click(function () {
        $('#kindscover').hide();
        $('#kindsmodal').hide();
    })
    $('#kindsmodal .modal_content .Button input[value="取消"]').click(function () {
        $('#kindscover').hide();
        $('#kindsmodal').hide();
    })

    /**报名信息的学生添加 */
    $('.registrationAddInfomation .addButton').click(function () {
        $('#Topcover').show()
        $('#Topmodal').show();
    })
    $('#baseStudentclose').click(function () {
        $('#Topcover').hide();
        $('#Topmodal').hide();
    })



    /**学生信息详情的改动 */
    $('.studentDetail .detailContent .applyTitle .showOrHide').click(function () {
        $('.studentDetail .detailContent .applyTitle ul').toggle()
        $('.studentDetail .detailContent .applyTitle .showOrHide').toggle()

    })
    $('.studentDetail .detailContent .classTitle .showOrHide').click(function () {
        $('.studentDetail .detailContent .classTitle ul').toggle()
        $('.studentDetail .detailContent .classTitle .showOrHide').toggle()
    })

    /**教师信息详情的改动 */
    $('.teacherDetail .detailContent .applyTitle .showOrHide').click(function () {
        $('.teacherDetail .detailContent .applyTitle ul').toggle()
        $('.teacherDetail .detailContent .applyTitle .showOrHide').toggle()

    })
    $('.teacherDetail .detailContent .classTitle .showOrHide').click(function () {
        $('.teacherDetail .detailContent .classTitle ul').toggle()
        $('.teacherDetail .detailContent .classTitle .showOrHide').toggle()
    })


    /**报名信息的添加弹框 */
    $('.registrationInformationTitle .registrationLeft input[value="添加"]').click(function () {
        $('#registrationcover').show();
        $('#registratiomodal').show()
    })
    /**关闭添加弹框 */
    $('#registrationclose').click(function(){
        $('#registrationcover').hide();
        $('#registratiomodal').hide()
    })

    $('.registrationAdd .saveButton input[value="取消"]').click(function () {
        $('#registrationcover').hide();
        $('#registratiomodal').hide();
    })

    /**报名信息的编辑弹框 */
    $('.registrationInformationTitle .registrationLeft input[value="编辑"]').click(function () {
        $('#registrationEditcover').show();
        $('#registrationEditmodal').show()
    })
    $('#registrationEditclose').click(function(){
        $('#registrationEditcover').hide();
        $('#registrationEditmodal').hide()
    })
    $('.regidtrationEdit .saveButton input[value="取消"]').click(function () {
        $('#registrationEditcover').hide();
        $('#registrationEditmodal').hide()
    })


        /**报名信息的导出弹框的删除按钮 */
    $('#registermodal .modal_button input[value="取消"]').click(function () {
        restritration();
    })


   /**报名信息备注过长的问题 */
     $('.mouseover').mouseover(function(){
         $(this).find('p').css("display","block").css('cursor',"pointer")
     })
     $('.mouseover').mouseout(function(){
        $(this).find('p').css("display","none")
    })

     $('.registrationInformationTitle .registrationLeft input[value="导出"]').click(function(){
      if($('.registrationContent .conytentMain input[type="checkbox"]').is(':checked') == true){
        $('#registercover').show()
        $("#registermodal").show()
      }
  })


  $('.tiaoshi .paddingLeft input[value="导出"]').click(function(){
      if($('.tiaoshi .mainContent input[type="checkbox"]').is(':checked') == true){
        $('#cover').show()
        $("#modal").show()
      }
  })


  $('.studentBig .paddingLeft input[value="导出"]').click(function(){
    if($('.studentBig .studentContent input[type="checkbox"]').is(':checked') == true){
        $('#studentcover').show()
        $("#studentmodal").show()
    }
})
$('.teacherNew .paddingLeft input[value="导出"]').click(function(){
    if($('.teacherNew .mainContent input[type="checkbox"]').is(':checked') == true){
        $('#teachercover').show()
        $("#teachermodal").show()
    }
})

//课程类型选择
  var items=$('.sideContent .registration .registrationInformation .registrationRight .hoverLi .hover li .first')
    var itemsOne=$('.sideContent .tiaoshi .contentHead .padding_right .hoverLi .hover li .first')
   function seleect(element) {
         var k=26;
  for(var i=0;i<element.length;i++) {
      $(element[0]).css('top', 0)
      if (i > 0) {
          $(element[i]).css('top', k * i)
      }
    }
   };

     seleect(items);
     seleect(itemsOne);


     /*上课信息的课程信息的文字回填*/
     $('.tiaoshi .clickHover input').mouseover(function () {
         $('.tiaoshi .clickHover .hover').show();
     })



    var textReturn=$('.tiaoshi .clickHover .third li')
    for(var i=0;i<textReturn.length;i++){
        $(textReturn[i]).click(function () {
            $('.tiaoshi .clickHover input').val('')

              textOne=$(this).text().trim();
              textTwo=$(this).parents('.f_child').clone().children().remove().end().text().trim();
               //给隐藏的课程input和课程类型input赋值
            $("input[name='course_id']").val($(this).parents('.f_child').clone().children().remove().end().attr("course_id"))
            $("input[name='course_type_id']").val($(this).attr("course_type_id"))
            $('.tiaoshi .clickHover input').val( textTwo + "(" + textOne + ")" )
             $('.tiaoshi .clickHover .hover').hide();
        })
    }

    /*报名信息的课程信息的文字回填*/

     $('.registrationRight .clickHover input').mouseover(function () {
         $('.registrationRight .clickHover .hover').show();
     })

  var Return=$('.registrationRight .clickHover .third li')
    for(var i=0;i<Return.length;i++){
        $(Return[i]).click(function () {
            $('.registrationRight .clickHover input').val('')

              textOne=$(this).text().trim();
              textTwo=$(this).parents('.f_child').clone().children().remove().end().text().trim();
              //给隐藏的课程input和课程类型input赋值
            $("input[name='course_id']").val($(this).parents('.f_child').clone().children().remove().end().attr("course_id"))
            $("input[name='course_type_id']").val($(this).attr("course_type_id"))
            $('.registrationRight .clickHover input').val( textTwo + "(" + textOne + ")" )
            $('.registrationRight .clickHover .hover').hide();
        })
    }

   /** 报名信息胡顶级弹框胡取消按钮*/
        $('#Topmodal .TopModal_content input[value="取消"]').click(function () {
          $('#Topcover').hide();
          $('#Topmodal').hide();
           $('#Topmodal .TopModal_content input[type="checkbox"]').attr("checked", "checked").prop('checked', false);
    })
})