

function add_btn_listerners(){
for (const bookButton of document.querySelectorAll('.add_book_btn')) {
  
  bookButton.addEventListener('click',evt => {
    evt.preventDefault();
    
    const formInputs = {
      book_id: bookButton.value
    }
    console.log(formInputs)
    fetch('/push_into_shelf', {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
              'Content-Type': 'application/json',              
            },
            // credentials:"same-origin"
          })
            .then(response => response.json())
            .then(responseJson => {
              bookButton.disabled = true
              alert(responseJson.status)
            });



  });
}}