<script>
  $( function() {
    var availableTags = [
      "workout",
      "yoga", 
      "run"
    ];
    $( "#activity_query" ).autocomplete({
      source: availableTags
    });
  } );
  </script>