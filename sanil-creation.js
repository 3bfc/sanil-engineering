var sanil = (function($) {
  var collective = ""; // Initialize collective variable

  function setCollective(value) {
      collective = value;
  }

  function privateFunction() {
      // Code for private function goes here
  }

  return {
      init: function(options) {
          // Initialize your library with options
          if (options.collective) {
              setCollective(options.collective);
          }
          console.log("Initializing MyLibrary with options:", options);
          privateFunction();
      },
      doSomething: function() {
          console.log("Doing something...");
      }
  };
})(jQuery);