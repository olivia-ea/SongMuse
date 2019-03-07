"use strict";
  

$( function() {
  var availableTags = [
    "workout", "yoga", "run", "70s music", "80s music", "90s music", "Disney",
    "Road Trip", "rock", "hip-hop", "country"
  ];

  $("#activity_query").autocomplete({
    source: availableTags
  });
});

