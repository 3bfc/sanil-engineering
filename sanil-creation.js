/* 
  PURPOSE: this library adds essential event listeners 
  NOTE: add this library at the end
*/

var sanil = (function($) {
  var collective = ""; // Initialize collective variable
  var $packageRadios = $('input[name="package"]');
  var $form = $('#wf-form-Sponsorship');
  var $submitBtn = $('#submit');
  
  // updates the text field that is visible to the user
  var $packageLabel = $('#package-label');
  
  // updates the form input that matches the MS custom field
  var $planIntent = $('#plan-intent');

  var $form = $('#wf-form-Sponsorship');

  function init(options) {
    // Initialize your library with options
    if (options.collective) {
      set_collective(options.collective);
      initialize_listeners();
    }
    console.log("Initializing sanil with options:", options);
  }

  function update_package_display() {
    var package_name = $packageRadios.filter(':checked').attr('package-name');
    $packageLabel.text(package_name);
    $planIntent.val(package_name)
  }

  function initialize_listeners() {
    update_package_display();

    // listens to changes on the radio cards
    $packageRadios.on('change',function() {
      update_package_display();
      var new_price_id = $(this).val();
      $submitBtn.attr('data-ms-price:add', new_price_id);
      alert(new_price_id)
    })
  }

  function set_collective(value) {
    collective = value;
  }
  return {
      init: init,
      doSomething: function() {
          console.log("Doing something...");
      }
  };
})(jQuery);