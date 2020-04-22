// cookies
window.addEventListener("load", function(){
  window.wpcc.init({
    "colors":{
    "popup":{
    "background":"#fff2cc",
    "text":"#101010",
    "border":"#fff2cc"
    },
    "button":{
      "background":"#247971",
      "text":"#ffffff"
    }
    },
    "position":"bottom",
    "margin":"none",
    "transparency":"40",
    "content":{
      "message":"We care about your data, and we'd use cookies 🍪 only to improve your experience:",
      "link":"Cookie Policy.",
      "button":"Okay, sure! 🦁",
      "href":"/cookie-policy"
    }
  })
});

// Form Homepage
    function myFunction() {
        var email = document.forms["myForm"]["sub_email"].value;
        if (validate(email) && document.getElementById('field_terms').checked) {
            $('#myModal').modal('show');
        }
        else {
            return false;
        }
    }
    function myFunction1() {
        var email = document.forms["myForm1"]["sub_email1"].value;
        if (validate(email) && document.getElementById('field_terms1').checked) {
            $('#myModal').modal('show');
        }
        else {
            return false;
        }
    }
    function closeModal() {
        document.getElementById("myForm").reset();
        document.getElementById("myForm1").reset();
    }
    function validate(email) {
        var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{1,4})$/;
        if (reg.test(email) == false) {
            return false;
        } else {
            return true;
        }
    }

    window.addEventListener("DOMContentLoaded", function(e) {
        var myForm = document.getElementById("myForm");
        var checkForm = function(e) {
            //...
            if(!this.terms.checked) {
                alert("Please indicate that you accept the Terms and Conditions");
                this.terms.focus();
                e.preventDefault(); // equivalent to return false
                return;
            }
        };

        // attach the form submit handler
        myForm.addEventListener("submit", checkForm, false);

        var myCheckbox = document.getElementById("field_terms");
        var myCheckboxMsg = "Please indicate that you accept the Terms and Conditions";

        // set the starting error message
        myCheckbox.setCustomValidity(myCheckboxMsg);

        // attach checkbox handler to toggle error message
        myCheckbox.addEventListener("change", function(e) {
            this.setCustomValidity(this.validity.valueMissing ? myCheckboxMsg : "");
        }, false);

    }, false);

// Form Partnerships
    function myFunction() {
        var name = document.forms["contact_workshop"]["fname"].value;
        var email = document.forms["contact_workshop"]["email"].value;
        if (name!="" && validate(email) && document.getElementById('field_terms').checked) {
            $('#myModal').modal('show');
        }
        else {
            return false;
        }
    }
    function closeModal() {
        document.getElementById("contact_workshop").reset();
        window.location.href = "/";
    }
    function validate(email) {
        var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{1,4})$/;
        if (reg.test(email) == false) {
            return false;
        } else {
            return true;
        }
    }

// Form Therapists
    function myFunction() {
        var name = document.forms["contact_workshop"]["fname"].value;
        var email = document.forms["contact_workshop"]["email"].value;
        if (name!="" && validate(email) && document.getElementById('field_terms').checked) {
            $('#myModal').modal('show');
        }
        else {
            return false;
        }
    }
    function closeModal() {
        document.getElementById("contact_workshop").reset();
        window.location.href = "/";
    }
    function validate(email) {
        var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{1,4})$/;
        if (reg.test(email) == false) {
            return false;
        } else {
            return true;
        }
    }


// Form Workshops
    function myFunction() {
        var name = document.forms["contact_workshop"]["fname"].value;
        var email = document.forms["contact_workshop"]["email"].value;
        if (name!="" && validate(email) && document.getElementById('field_terms').checked) {
            $('#myModal').modal('show');
        }
        else {
            return false;
        }
    }
    function closeModal() {
        document.getElementById("contact_workshop").reset();
        window.location.href = "/";
    }
    function validate(email) {
        var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{1,4})$/;
        if (reg.test(email) == false) {
            return false;
        } else {
            return true;
        }
    }


// nav
$(document).ready(function() {
  $(".navbar a").on('click', function(event) {
    if (this.hash !== "") {
      event.preventDefault();
      var hash = this.hash;
      var ht = $(".navbar-fixed-top").height() - 50;
      var val = $(hash).offset().top;
      $('html, body').unbind().animate({
        scrollTop: val
      }, 500, function() {
        window.location.hash = hash;
      });
    }
  });

  $('.navbar-nav>li>a').on('click', function() {
    $('.navbar-collapse').collapse('hide');
  });

  $('.hidden').fadeIn(4000).removeClass('hidden');
  $('h1').fadeIn(4000).removeClass('hiddenA');
  $('p').fadeIn(4000).removeClass('hiddenB');
});

