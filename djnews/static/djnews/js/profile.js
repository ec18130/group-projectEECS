const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value; // get csrftoken from DOM


$(document).ready(function () {
    let $form = ($("#favourite-category-form"));
    $form.submit(function (e){
        return false;
    });
    let favouriteCategoryCheckboxes = $('.favourite-category-checkbox')
    for (let i = 0; i < favouriteCategoryCheckboxes.length; i++){
        favouriteCategoryCheckboxes[i].checked=false;
    }
    for (let i = 0; i < favouriteCategories.length; i++){
        for (let a = 0; a < favouriteCategoryCheckboxes.length; a++){
            if(favouriteCategoryCheckboxes[a].value == favouriteCategories[i]){
                favouriteCategoryCheckboxes[a].checked = true;
            }
        }
    }
});

function saveFavourites(){
    let formData = $("#favourite-category-form").serializeArray();
    let formDataArray = []
    for(let i = 0; i < formData.length; i++){
        formDataArray.push(formData[i].value);
    }

    let data = {
        'favouriteCategories' : formDataArray
    }

    //construct request
    const request = new Request(
        "/profile/" + profileId + "/",

        {
            headers: {"X-CSRFToken": csrftoken},
        }
    );
    //execute request
    fetch(request, {
        // execute fetch request
        method: "POST",
        mode: "same-origin",
        body: JSON.stringify(data),
    }).then(res => res.json().then(json => {
        $('#favourites-updated-text').text(json.message)
    }));
}

