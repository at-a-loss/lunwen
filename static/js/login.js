/**
 * Created by lenovo on 2019/12/8.
 */
$(function () {
    $("#name").blur(function () {
        var xhr
        if(window.ActiveXObject){
            xhr=new ActiveXObject("Microsoft.XMLHTTP")
        }else if(window.XMLHttpRequest){
            xhr=new XMLHttpRequest()
        }
        xhr.open("get","/ems/loginAjax/?name="+$("#name").val())
        xhr.send()
        xhr.onreadystatechange=function () {
            if(xhr.readyState==4 && xhr.status==200){
                if(xhr.responseText==""){
                    $("#rpw").prop("checked",false)
                    $("#pw").val(xhr.responseText)
                }else{
                    $("#rpw").prop("checked",true)
                    $("#pw").val(xhr.responseText)
                }
            }
        }
    })
})