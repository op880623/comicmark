function isMobileDevice() {
  return (typeof window.orientation !== "undefined")
      || (navigator.userAgent.indexOf('IEMobile') !== -1);
};

$(document).ready(function() {
  if (isMobileDevice()) {
    for (var i = 0; i < $("a[target=_blank]").length; i++){
      a = $("a[target=_blank]")[i];
      a.pathname = "/m" + a.pathname;
    }
  }

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
