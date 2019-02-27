<script>
  $( function() {
    var availableTags = [
      "Workout",
      "Yoga", 
      "Beach"
    ];
    $( "#activity_query" ).autocomplete({
      source: availableTags
    });
  } );
  </script>