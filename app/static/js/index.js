$(document).ready(function(){
  $(".bg-img").mouseenter(function(){
    $(this).next().show();
  })
  $(".des1").mouseleave(function(){
      $(this).hide();
    })

    $(".bg-img").mouseenter(function(){
      $(this).next().show();
    })
    $(".des2").mouseleave(function(){
        $(this).hide();
      })

        $(".bg-img").mouseenter(function(){
          $(this).next().show();
        })
        $(".des3").mouseleave(function(){
            $(this).hide();
          })
});