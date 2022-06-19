function bookSearch(evt){
    
    evt.preventDefault()
    const keyword = document.getElementById('s_key').value;
    
    const url = `/neighbor_search?keyword=${keyword}`;

    fetch(url)
        .then(response => response.json())
        .then(apiResponse => {
            console.log(apiResponse)
            const results = document.querySelector('#results')
                
            
            
            
            
                results.insertAdjacentHTML('beforeend',
            `<h3>Result</h3>
            <div>We found ${apiResponse.totalItems} books about "${keyword}"</div>
            <div>
           ${putings_res}
            </div>
            `)

            
              
                 
            //   add_btn_listerners();                    
        });
}



// document.querySelector('#search').addEventListener('submit',bookSearch);

// let myText = document.getElementById("");
let seform = document.getElementById("nei_search");

seform.addEventListener("submit",bookSearch);

