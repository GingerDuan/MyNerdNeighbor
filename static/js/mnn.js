function bookSearch(evt){
    evt.preventDefault();

    const keyword = document.querySelector('#my-text').value;
    // const url = `https://www.googleapis.com/books/v1/volumes?q=${keyword}`;
    const url= `/search?keyword=${keyword}`;
    fetch(url)
        .then(response => response.json())
        .then(apiResponse => {
            console.log(apiResponse)
            const results = document.querySelector('#results')
                results.innerHTML = ''
                results.insertAdjacentHTML('beforeend',
            `<h2>Result</h2>
            <div>We found ${apiResponse.totalItems} books about "${keyword}"</div>`)

            for (const book of apiResponse.items){
                let img = `<img src="https://icon-library.com/images/book-icon-png/book-icon-png-28.jpg" width="128" height="130">`
                
                if (book.volumeInfo.imageLinks){
                    img = `<img src="${book.volumeInfo.imageLinks.thumbnail} width="128" height="182">`
                }
                results.insertAdjacentHTML('beforeend',
                `<div class = bookContainer style = "margin: 15px">
                <span class = bookPic>
                ${img}
                </span>
                <span class = bookText overflow: hidden;
                text-overflow: ellipsis;
                max-width: 25ch>
                <a href=${book.volumeInfo.infoLink} target="_Blank">${book.volumeInfo.title}</a>
                ${book.volumeInfo.subtitle}
                <br>
                by: ${book.volumeInfo.authors}
                <button value = ${book.id}>put on my shelf</button>
                <br>
                <span style="display:inline-block;
                overflow: hidden;
                maxheight: 110px;">description:${book.volumeInfo.description}</span>
                <br>
                <button >I have read this book</button>
                <button >I am reading this book</button>
                <button >Add to want to list</button>
                </span></div>`);
                }                       
        });
}

// evt.preventDefault()

// document.querySelector('#search').addEventListener('submit',bookSearch);

let myText = document.getElementById("my-text");
let btn = document.getElementById("btn");

myText.addEventListener("keyup",e =>{
    e.preventDefault();
    if(e.keyCode ===13){
        bookSearch
        btn.click();
    }
})
btn.addEventListener("click",bookSearch);
