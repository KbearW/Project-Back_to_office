'use strict';

// /////////////////////////////////////////////////
// PRACTICE SOLUTIONS
// /////////////////////////////////////////////////

// Make an Event Handler

// The goal here is to make a simple event handler
// and use the alert() method

let button = document.querySelector('#popup-alert-button');
button.addEventListener('click', () => alert("Hi!"));

// It would also be fine to do this the following way:
//
//  button.addEventListener('click', function () { alert("Hi!"); }
// or to create a named function and pass the name as a callback:
// function alertMe(evt) {
//     alert("Hi!");
// }
// button.addEventListener('click', alertMe) 
// Note that we are just passing in the alertMe function as an argument (not calling it)

// Practice Your Times Tables

// The goal here is to practice evt.preventDefault, using JS to do small
// programming tasks, and adding content to the DOM

let multForm = document.querySelector("#multiplying-form");
multForm.addEventListener("submit", function (evt) {

    evt.preventDefault();

    let multsOf = parseInt(document.querySelector("#mults-of").value);
    let max = parseInt(document.querySelector("#max").value);
    let multiples = [];
    let nextMult = multsOf;

    while (nextMult <= max) {
      multiples.push(nextMult);
      nextMult = nextMult + multsOf;
    }

    console.log(multiples);
});



// Finding the Button

// The goal here is to use the right DOM method to get the items by
// class and then to index that, since it will always be a list

function alertMeThree(evt) {
    alert("Ok, you found it!");
}

$('.find-me').on('click', alertMeThree);


// Slowly Make a Porcupine


$('#make-a-porcupine').on('click', () => $('#cute-porcupine-image').delay(1000).slideDown(2000));
// $('#make-a-porcupine').on('click', () => setTimeout(() => $('#cute-porcupine-image').slideDown(2000), 1000));
//$('#make-a-porcupine').on('click',
//    function (evt) {
//        setTimeout(
//            function () {
//                $('#cute-porcupine-image').slideDown(2000);
//            }, 1000
//        )
//    }
//);


// An Agreeable Form

// The goal here is to learn about .val() and practice .html()

function agree(evt) {
    evt.preventDefault();
    let theirFood = $('#favorite-food-input').val();
    $('#agreeable-text').html(`I like ${theirFood}, too!`);
}

$('#agreeable-form').on('submit', agree);


// Five colored primes

function isPrime(x) {
    // is X prime?

    for (let i = 2; i * i <= x; i++) {
        if (x % i === 0) {
            return false;
        }
    }
    // We never found a divisor, so it's prime
    return true;
}

function makePrimes(evt) {
    let num = 2;     // find primes higher than 1
    let numFound = 0;
    $('#prime-circle-area').html('');
    while (numFound < 5) {
        if (isPrime(num)) {
            $('#prime-circle-area').append(
                `<div class='prime-circle' style='background-color:
                ${PRIME_COLORS[numFound]}'>${num}</div>`);
            numFound = numFound + 1;
        }
        num = num + 1;
    }
}

$('#make-prime-circles').on('click', makePrimes);

// Got Puppies?

$("#puppy-form").submit(function (evt) {

    //prevent the form from triggering a page load
    evt.preventDefault();

    //get data from the form and package it up in an object to be sent with
    //the AJAX request
    let numPuppies = $("#num-puppies").val();
    let data = {"num-puppies": numPuppies};

    //make the AJAX request
    $.get("/puppies.json", data, showPuppies);

});
