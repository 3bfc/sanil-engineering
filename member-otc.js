$(document).ready(function() {
  // Track changes in the radio group
//        $('#prc_monthly-i3f609sy').prop("checked", true);

  var attrValue = $('input[name="package"]:checked').attr("package-name");
  $('#package-label').text(attrValue);
  $('#plan-intent').val(attrValue);
  var selectedValue = $('input[name="package"]:checked').val();
  $('#submit').attr('data-ms-price:add', selectedValue);
   $('input[name="package"]').on('change', function() {
     var attrValue = $('input[name="package"]:checked').attr("package-name");
    $('#package-label').text(attrValue);
    console.log(attrValue);
  });
  $('#otc-link').on('click',function(e){
    var selectedValue = $('input[name="package"]:checked').val();
    var sport = $('#field').val();
    $('#otc-link').attr('href',selectedValue);
  });

});
