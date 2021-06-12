

//This file MUST be in Static due to the stack structure!
// alert('js connected')
console.log('yes, form.js is working')

const form = document.getElementById('form');
const company = document.querySelector('#company');
const address = document.querySelector('#address');
const ratings = document.getElementsByName("rating");
const para = document.querySelector('p');

company.placeholder = 'Company Name'
address.placeholder = 'Street, City, State'


form.onsubmit = function(e) {
  // e.preventDefault();
  // console.log('yes')  ;
  function radioChecked (e){      
                              for (var i=0, len=ratings.length; i<len; i++){
                                  if (ratings[i].checked){
                                    console.log('true')
                                    return true;
                                  }
                               }
                                para.textContent='false';
                                return false;
                          }

        if (company.value === '' || address.value === '' || radioChecked() === false
        ) {
          e.preventDefault();
          para.textContent = 'Please fill out all fields!~~~~~(IN RED)';
        }
  }
