const exampleModal = document.getElementById('exampleModal')
exampleModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  const button = event.relatedTarget
  // Extract info from data-bs-* attributes
  const recived = button.getAttribute('data-bs-whatever')
  const book_id = button.getAttribute('value')
  // If necessary, you could initiate an AJAX request here
  // and then do the updating in a callback.
  //
  // Update the modal's content.
  radio_id = "#"+recived
  const status_f = exampleModal.querySelector(radio_id)
  const submit_btn = exampleModal.querySelector('#submit')
  
//   const modalBodyInput = exampleModal.querySelector('#note-text')
    status_f.checked = true;
    submit_btn.value = book_id

})
