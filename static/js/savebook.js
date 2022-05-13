

const get_googlebook_id = (evt) => {
    

    const formInputs = {
      googlebook_id: evt.target.value
    }
    console.log(formInputs)


    fetch('/put_into_shelf', {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
              'Content-Type': 'application/json',              
            },
          })
            .then(response => response.json())
            .then(responseJson => {
              // bookButton.disabled = true
              alert(responseJson.status);
            });
};
for (const bookButton of document.querySelectorAll('.add_book_btn')){
  bookButton.addEventListener('click',evt => {
    
    // evt.target.disabled = true;
    get_googlebook_id(evt);
  })
}
  
