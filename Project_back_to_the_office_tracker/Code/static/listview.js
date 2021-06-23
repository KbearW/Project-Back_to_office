

//This file MUST be in Static due to the stack structure!
// alert('js connected')

const form = document.getElementById('form');
const search = document.querySelector('#search');
const para = document.querySelector('p');
const company = document.getElementsByTagName('td');

//This is close... click on any box, a popup will tell you the value within the box
var t = document.getElementById("table");
var trs = t.getElementsByTagName("tr");
var search_key = null;
var tds = 'Facebook';
// console.log(search)

// form.onsubmit = function(e) {
    
//     if (search.value === ""
//         ) {
//         e.preventDefault();
//         para.textContent = 'Enter something';
//         }
//         //Else if doesn't work....
//     else if ( 
//         //Where to put the below?
//     //     for (var i=0; i<trs.length; i++)
//     //         var tds = trs[i].getElementsByTagName("td")[1]
//                search.value === tds
//             )
//                     {        
//                         e.preventDefault();
//                         // still need some work to only filter on the search
//                         alert(tds.innerHTML); 
//                     }
//     else {
//         e.preventDefault();
//         para.textContent = "This company doesn't exist in the database.";
//         };
            
//         console.log(search_key);
        
//     };

    function sortTable_rating() {
        var table, rows, switching, i, x, y, shouldSwitch;
        table = document.getElementById("table");
        switching = true;
        /*Make a loop that will continue until
        no switching has been done:*/
        while (switching) {
          //start by saying: no switching is done:
          switching = false;
          rows = table.rows;
          /*Loop through all table rows (except the
          first, which contains table headers):*/
          for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("td")[2];
            y = rows[i + 1].getElementsByTagName("td")[2];
            //check if the two rows should switch place:
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
              //if so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
          if (shouldSwitch) {
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
          }
        }
      };


    function sortTable_company_name() {
        var table, rows, switching, i, x, y, shouldSwitch;
        table = document.getElementById("table");
        switching = true;
        /*Make a loop that will continue until
        no switching has been done:*/
        while (switching) {
          //start by saying: no switching is done:
          switching = false;
          rows = table.rows;
          /*Loop through all table rows (except the
          first, which contains table headers):*/
          for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("td")[0];
            y = rows[i + 1].getElementsByTagName("td")[0];
            //check if the two rows should switch place:
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
              //if so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
          if (shouldSwitch) {
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
          }
        }
      };


      // function sortTable_office_lcoation() {
      //   var table, rows, switching, i, x, y, shouldSwitch;
      //   table = document.getElementById("table");
      //   switching = true;
      //   /*Make a loop that will continue until
      //   no switching has been done:*/
      //   while (switching) {
      //     //start by saying: no switching is done:
      //     switching = false;
      //     rows = table.rows;
      //     /*Loop through all table rows (except the
      //     first, which contains table headers):*/
      //     for (i = 1; i < (rows.length - 1); i++) {
      //       //start by saying there should be no switching:
      //       shouldSwitch = false;
      //       /*Get the two elements you want to compare,
      //       one from current row and one from the next:*/
      //       x = rows[i].getElementsByTagName("td")[1];
      //       y = rows[i + 1].getElementsByTagName("td")[1];
      //       //check if the two rows should switch place:
      //       if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
      //         //if so, mark as a switch and break the loop:
      //         shouldSwitch = true;
      //         break;
      //       }
      //     }
      //     if (shouldSwitch) {
      //       /*If a switch has been marked, make the switch
      //       and mark that a switch has been done:*/
      //       rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      //       switching = true;
      //     }
      //   }
      // }
        
      //Issue w this search functio- will only return the first result even w diff addresses
      function searchfunction() {
        var input, filter, table, tr, td, i, txtValue;
        input = document.getElementById("search");
        filter = input.value.toUpperCase();
        table = document.getElementById("table");
        tr = table.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
          td = tr[i].getElementsByTagName("td")[0];
          if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
              tr[i].style.display = "";
            } else {
              tr[i].style.display = "none";
            }
          }       
        }
      }

      