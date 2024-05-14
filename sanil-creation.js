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
      update_package_display();
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
  
    // listens to changes on the radio cards
    $packageRadios.on('change',function() {
      update_package_display();
      var new_price_id = $(this).val();
      $submitBtn.attr('data-ms-price:add', new_price_id);
    })

    $form.attr('action','#');
    $form.submit(function(event){
      event.preventDefault;
    })
    $form.submit(async function(event){
      event.preventDefault;
      try {
        var formData = $(this).serializeArray();
        var email = formData.find(item => item.name === 'email').value;
        var password = formData.find(item => item.name === 'password').value;
        var first = formData.find(item => item.name === 'first').value;
        var last = formData.find(item => item.name === 'last').value;
        var sport = formData.find(item => item.name === 'sport').value;
        var selectedValue = $packageRadios.filter(':checked').val();

        // Signup member
        await memberstack.signupMemberEmailPassword({
            customFields: {
                'plan-intent': $planIntent.val(),
                'sport-package': sport,
                'first-name': first,
                'last-name': last,
            },
            email: email,
            password: password
        });
asdfasdf
        // Purchase plans with checkout
        var domain = "https://" + window.location.hostname;
        await memberstack.purchasePlansWithCheckout({
            priceId: selectedValue,
            metadataForCheckout: {
                SPORT: sport,
                COLLECTIVE: collective
            },
            cancelUrl: domain,
            successUrl: domain,
            autoRedirect: true
        });
    } catch (err) {
      displayErrorMessage(err.message);
    }
    });
  }

  function set_collective(value) {
    collective = value;
  }
  return {
      init: init
  };
})(jQuery);