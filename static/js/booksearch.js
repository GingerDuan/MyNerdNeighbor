function bookSearch(evt){
    


    evt.preventDefault()
    let keyword = document.getElementById('sss_key').value;
    
    const url = `/neighbor_search?keyword=${keyword}`;
    console.log(keyword)
    

    fetch(url)
        .then(response => response.json())
        .then(apiResponse => {
            

            const putings = apiResponse.putings
            const results = document.querySelector('#n_results')
                
            
            
            
            
                results.innerHTML=
            `<h3>Result</h3>
            <div>We found ${putings.length} books about "${keyword}"</div>
            <div>
           ${putings}
            </div>`

            
              
                 
            //   add_btn_listerners();                    
        });
}



// document.querySelector('#search').addEventListener('submit',bookSearch);

// let myText = document.getElementById("");
let seform = document.getElementById("nei_search");

seform.addEventListener("submit",bookSearch);

