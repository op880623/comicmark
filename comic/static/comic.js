$(document).ready(function() {
  $("button.read-now").click(function(event) {
    event.target.parentElement.parentElement.children[0].click();
    event.target.parentElement.children[0].click();
  });

  $("button.close").click(function(event) {
    var ans = confirm("確定刪除？");
    if (ans == true) {
      event.target.nextElementSibling.click();
    }
  });
});
