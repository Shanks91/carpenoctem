/**
 * Created by Harshank Kahar on 09-05-2017.
 */

$(document).ready(function() {
    $(".clickable-row").click(function() {
      window.location = $(this).data("href");
    });
});
