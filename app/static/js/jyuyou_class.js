function chkselect() {
    $val = $("select[name='jiki']").val();

    if($val == 'year'){
        document.getElementById("number_input").style.display="block";
    }else {
        document.getElementById("number_input").style.display="none";
    }

    if($val == 'summer'){
        document.getElementById("summer_number_input").style.display="block";
    }else {
        document.getElementById("summer_number_input").style.display="none";
    }

    if($val == 'winter'){
        document.getElementById("winter_number_input").style.display="block";
    }else {
        document.getElementById("winter_number_input").style.display="none";
    }
}