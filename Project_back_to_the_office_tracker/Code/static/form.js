

//This file MUST be in Static due to the stack structure!
// alert('js connected')
console.log('yes, form.js is working')

const form = document.getElementById('form');
const company = document.querySelector('#company');
const address = document.querySelector('#address');
const rating = document.getElementsByName('rating');
const para = document.querySelector('p');

company.placeholder = 'Company Name'
address.placeholder = 'Street, City, State'


form.onsubmit = function(e) {
  // e.preventDefault();
  // console.log('yes')  
  // rating.value doesn' work.... radio button--> "checked"- look into it
  if (company.value === '' || address.value === '' || rating.value === '') {
      e.preventDefault();
      para.textContent = 'You need to fill in both names!';
    }
  }
