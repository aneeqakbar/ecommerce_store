const fetchPage = async (url) =>{
    return fetch(url,  {
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

let counter = 1
let end = false


let loadMoreProducts = async (baseUrl,recommendations__products,loadMoreSpinner)=>{
    url = `${baseUrl}?page=${counter}`
    loadMoreSpinner.style.display = 'inline-block'
    await fetchPage(url).then(async (res)=>{
        setTimeout(async ()=>{
            loadMoreSpinner.style.display = 'none'
            if (res.ok) {
                content = await res.text()
                recommendations__products.innerHTML += content;
            }else{
                end = true
            }
        },500)
    })
}

let loadMoreClickHandler = async (baseUrl,recommendations__products,no_more_indicator,loadMoreSpinner)=>{
    if (!end) {
        counter += 1;
        await loadMoreProducts(baseUrl,recommendations__products,loadMoreSpinner);
    }else{
        if (no_more_indicator != null) {
            no_more_indicator.style.display = 'block';
            setTimeout(()=>{
                no_more_indicator.style.display = 'none';
            },800)
        }
    }
}