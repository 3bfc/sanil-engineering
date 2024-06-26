$(document).ready(function () {
  $('#submit').prop('disabled', true);
  memberstack.getCurrentMember().then((member) => {
    var active_account = true;

    if (member.data.planConnections.length > 0) {
      // if there is a plan
      var hasActivePlan = false; // Flag to check if there's at least one active plan
      $.each(member.data.planConnections, function (index, item) {
        // if plan is active
        if (item.status === "ACTIVE") {
          hasActivePlan = true; // Set flag if an active plan is found
          return false; // Exit loop early since we found an active plan
        }
      });

      if (hasActivePlan) {
        console.log("active plan")
        $('#update-form').addClass('hidden');
      } else {
        $('#notification').addClass('hidden');
        $('#submit').prop('disabled', false);
        $('#submit').removeClass('button-secondary').addClass('button-primary');
      }
    } else {
      $('#notification').addClass('hidden');
      $('#submit').prop('disabled', false);
      $('#submit').removeClass('button-secondary').addClass('button-primary');
    }

    var attrValue = $('input[name="package"]:checked').attr("package-name");
    $('#package-label').text(attrValue);
    $('#plan-intent').val(attrValue);
    var selectedValue = $('input[name="package"]:checked').val();
    $('#submit').attr('data-ms-price:update', selectedValue);
    $('input[name="package"]').on('change', function () {
      // Get the value of the checked radio button
      var selectedValue = $('input[name="package"]:checked').val();

      // Set the custom attribute of the element
      $('#submit').attr('data-ms-price:update', selectedValue);
      var attrValue = $('input[name="package"]:checked').attr("package-name");
      $('#package-label').text(attrValue);
      $('#plan-intent').val(attrValue);
    });
  });
});
