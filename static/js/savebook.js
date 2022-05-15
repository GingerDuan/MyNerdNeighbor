

const get_googlebook_id = (evt) => {
    
    

    const formInputs = {
      googlebook_id: evt.target.value,
      title: document.querySelector('.book_title').innerHTML,
      author: document.querySelector('#book_authors').innerHTML,
      cover: document.querySelector('.book_img').src,
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
              
              alert(responseJson.status);
              

            });
};
for (const bookButton of document.querySelectorAll('.add_book_btn')){
  bookButton.addEventListener('click',evt => {
    // bookButton.disabled = true
    // evt.target.disabled = true;
    get_googlebook_id(evt);
  })
}
  
