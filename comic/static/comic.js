$(document).ready(function() {
  $("div.read-now").click(function(event) {
    event.target.parentElement.children[0].click();
    event.target.parentElement.children[1].click();
  });
});
