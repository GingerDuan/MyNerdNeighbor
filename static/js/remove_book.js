const get_book_id = (evt) => {
    
    const formInputs = {
      book_id: evt.target.value,
      
    }
    console.log(formInputs)

    fetch('/remove_from_shelf', {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
              'Content-Type': 'application/json',              
            },
          })
            .then(response => response.json())
            .then(responseJson => {  

              document.getElementById(evt.target.value).style.display = 'none'        
              // alert(responseJson.status);
              // docume get element by id, element.style,disaplay, none..  hidd the react visiblity 

            });
};


for (const bookButton of document.querySelectorAll('.remove_book_btn')){
  bookButton.addEventListener('click',evt => {
    
    get_book_id(evt);
    bookButton.disabled = true
    
  })
}