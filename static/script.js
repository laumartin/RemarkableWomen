
// To initialise the bootstrap library ekkolightbox, using event listener on the <a>tags with data-toggle=lightbox 
// to prevent the default behaviour (navigate to an URL). Then it initializes the lightbox.
$(document).on("click", '[data-toggle="lightbox"]', function(event) {
  event.preventDefault();
  $(this).ekkoLightbox();
});

// To use the select country bootstrap package 
$('.countrypicker').countrypicker();

// Characters page see more details of each card toggle
$("linktext").click(function(){
    $("fulltext").toggle();
});



