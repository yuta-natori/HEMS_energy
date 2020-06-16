function clickNormarized() {
    document.getElementById("histogram_img").style.display="none";
    document.getElementById("normarized_img").style.display="block";
    var elements = document.getElementsByClassName("profile_img");
    
    for(var i = 0; i < elements .length; i++) {
        elements[i].style.display = "none";
    }
}

function clickProfiles(month) {
    document.getElementById("histogram_img").style.display="none";
    document.getElementById("normarized_img").style.display="none";
    var elements = document.getElementsByClassName("profile_img");
    
    for(var i = 0; i < elements.length; i++) {
        if (i+1 == month) {
           elements[i].style.display = "block";
        } else {
            elements[i].style.display = "none";
        }
    }
}

function clickHistogram() {
    document.getElementById("histogram_img").style.display="block";
    document.getElementById("normarized_img").style.display="none";
    var elements = document.getElementsByClassName("profile_img");
    
    for(var i = 0; i < elements .length; i++) {
        elements[i].style.display = "none";
    }
}