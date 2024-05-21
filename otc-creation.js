/* 
  PURPOSE: this library adds essential event listeners 
  NOTE: add this library at the end
*/

var sanil = (function($) {
  // Initialize collective variable
  var collective = "";
  
  var $packageRadios = $('input[name="package"]');
  
  // updates the text field that is visible to the user
  var $packageLabel = $('#package-label');
  
  // updates the form input that matches the MS custom field
  var $planIntent = $('#plan-intent');


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
    })

    $('#otc-submit').on('click', async function(event) {
      try {
        var domain = "https://" + window.location.hostname;
        var price_id = $('input[name="package"]').filter(':checked').val();
        var sport = $('#sport').val();
        // After successful signup, redirect them to the stripe checkout
        await memberstack.purchasePlansWithCheckout({
          priceId: price_id,
          metadataForCheckout: {
            SPORT: sport,
            COLLECTIVE: collective
          },
          cancelUrl: domain,
          successUrl: domain,
          autoRedirect: true // Set this to true if you want to automatically redirect after successful purchase
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