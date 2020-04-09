  
  
<script type='text/javascript'>
jQuery(function() {
  $("#accordion li ul").hide();
  $("#active").show();
  $("#accordion > li > a").click(function(){
    var click = $("+ul",this);
    click.slideDown();
  $("#accordion ul").not(click).slideUp();
  $(".arrow").removeClass("rotate");
  $("> .arrow",this).addClass("rotate");
    return false;
  });
})(jQuery);
</script>
