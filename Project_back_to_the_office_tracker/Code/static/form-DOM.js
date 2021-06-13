
const form = document.querySelector('form');
const fname = document.getElementById('fname');
const lname = document.getElementById('lname');
const para = document.querySelector('p');

form.onsubmit = function(e) {
  if (fname.value === '' || lname.value === '') {
    e.preventDefault();
    para.textContent = 'You need to fill in both names!';
  }
}

// console.log('yes, form.js is working')

// const button = document.getElementById('#submit');
// const company = document.querySelector('#company');
// const address = document.querySelector('#address');
// // const rating = document.getElementByName('rating');
// const para = document.querySelector('p');

// company.value = 'Company Name'
// address.value = 'Street, City, State'


// button.onsubmit = function(e) {
//     if (company.value === '' || address.value === '') {
//       e.preventDefault();
//       para.textContent = 'You need to fill in both names!';
//     }
//   }