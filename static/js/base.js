/**
 * Created by lenovo on 2019/12/6.
 */
$(function () {
    setInterval(function () {
        var d=new Date()
        var time=d.getFullYear()+"/"+(d.getMonth()+1)+"/"+d.getDate()+" "+d.getHours()+":"+d.getMinutes()+":"+d.getSeconds()
        $("#time").html(time)
    },1000)
})