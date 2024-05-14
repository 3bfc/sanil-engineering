/* 
  PURPOSE: this is to handle all of the stuff with 
  NOTE: 
  – add this library at the end
  - the webflow ui handles the actual update of the MS custom field
  IMPROVEMENTS:
  - check with memberstack to see if there is a way to update the metadata after purchase
*/
var sanil_edit_sport = (function($){
  var $submitBtn = $('#submit');
  var $select = $('#field-2')
  var original_value = $select.val();

  function init(){
    $submitBtn.prop('disabled', true);
    initialize_listeners();
  }

  function initialize_listeners(){
    var sport = null
    $select.change(function () {
      // Check if an option other than the default one is selected
      var $this = $(this).val();
      sport = $this;
      if ($this !== original_value && $this !== '') {
        // Enable the button
        $submitBtn.prop('disabled', false);
        $submitBtn.removeClass('button-secondary').addClass('button-primary');
      } else {
        // If default option is selected, disable the button
        $submitBtn.prop('disabled', true);
        $submitBtn.removeClass('button-primary').addClass('button-secondary');
      }
    });
    
    $submitBtn.on('click', function(){
      var message = "Changed sport to " + sport;
      update_member_changelog(message)
    })
  }

  async function update_member_changelog(message) {
    const date = new Date();
    const dateString = date.toISOString();
    var entry = {
      'message': message,
      'date': dateString
    }
    if (typeof memberstack !== 'undefined') {
      var history = await memberstack.getMemberJSON();
    } else {
    	var history = undefined
    }

    if (history.data != undefined) {
      history.data.push(entry);
    } else {
      history = [entry];
    }

    await memberstack.updateMemberJSON({
      json: history
    });
    
  }
  return {
    init: init
  }
})(jQuery);