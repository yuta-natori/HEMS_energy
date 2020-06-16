window.onload = function() {
  chkselect()
}

function chkselect() {
    $val = $("select[name='season']").val();

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

function clickDistribution() {
    document.getElementById("distribution_img").style.display="block";
    document.getElementById("histogram_img").style.display="none";
}

function clickHistogram() {
    document.getElementById("distribution_img").style.display="none";
    document.getElementById("histogram_img").style.display="block";
}