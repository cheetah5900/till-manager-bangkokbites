"use strict";
var KTCreateDelivery = (function () {
  var e,
    t,
    r
  return {
    init: function () {
      (e = document.querySelector("#kt_modal_create_delivery")) &&
        new bootstrap.Modal(e),
        (t = document.querySelector("#kt_create_delivery_stepper")) &&
          ((r = new KTStepper(t)).on("kt.stepper.changed", function (e) {}),
          r.on("kt.stepper.next", function (e) {
            e.goNext();
          }),
          r.on("kt.stepper.previous", function (e) {
            e.goPrevious();
          }));
    },
  };
})();
KTUtil.onDOMContentLoaded(function () {
  KTCreateDelivery.init();
});
