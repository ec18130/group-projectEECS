const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value; // get csrftoken from DOM
let contentToRender;


$(document).ready(function () {
    populateInfo("favourites")
        .then(res => finishedLoading());
});

async function populateInfo(filter) {
    await populateArticles(filter);
    await populateComments();
    await populateLikes();
}

function finishedLoading() {
    console.log("Finished Loading");
}

async function populateArticles(filter) {
    let articleContainer = $('#article-container');
    articleContainer.children().remove();
    let request
    let articleHTML ="";

    if (filter == "all") {
        //Build request
        request = new Request(
            "/articles/",
            {
                headers: {"X-CSRFToken": csrftoken},
            }
        );
    } else {
        //Build request
        request = new Request(
            "/articles/"+ filter +"/",
            {
                headers: {"X-CSRFToken": csrftoken},
            }
        );
    }

    // Fetch articles
    await fetch(request, {
        method: "GET",
        mode: "same-origin"
    }).then(res => res.json().then(json => {
        articles = json.articles;
        console.log(articles)
        articleHTML += "<div class='row d-flex flex-column align-content-center'>"
        articleHTML += "<h3>" + filter.toUpperCase() + "</h3>";
        articleHTML += "</div>";
        articleHTML += "<div class='row d-flex flex-column align-content-center'>"
        if(articles.length == 0){
            if(filter=="favourites") {
                articleHTML += "<h3> There is no news in your favourite categories, add some more categories in your profile page!</h3>";
            }
             else {
                articleHTML+="<h3> No news in this category.</h3>";
            }
        }
        articleHTML += "</div>";
        articleHTML += "</div>";
        articleHTML += "<div class='list-group'>";
        for(let i = 0; i<articles.length; i++){
            articleHTML+="<div title='" + articles[i].id + "' class='article-list list-group-item bg-secondary text-light'>";
            articleHTML+="<h2>"+articles[i].title + "</h2>";
            articleHTML+="<h4>" + articles[i].category + "</h4>";
            articleHTML+="<h5>Written by "  + articles[i].author + " on "  + articles[i].date + "</h5>";
            articleHTML+="<p>" + articles[i].article + "</p>";
            articleHTML+="<button name='like-button-" + articles[i].id + "' class='like-button btn bg-dark text-light' onclick='handleLikesClick(" + articles[i].id + ")'>Likes:</button>";
            articleHTML+="<button class='add-comment-btn btn bg-dark bg-dark text-light' onclick='generateNewCommentForm(" + articles[i].id + ")'>Comment</button>";
            articleHTML+="<div title='" + articles[i].id + "' class='comments-container'></div>";
            articleHTML+="</div>";
            articleHTML+="<p><br></p>"
        }
        articleHTML += "<div>";
        articleContainer[0].innerHTML=articleHTML;
    }));

}

// Populates like likes button for each article on document ready
async function populateLikes() {
    let likeButtons = $('.like-button');
    for (let i = 0; i < likeButtons.length; i++) {
        await fetchLikes(likeButtons[i].name.match(/\d+/));
    }
}

// fetches likes for a single article
async function fetchLikes(articleId) {
    //Build request
    const request = new Request(
        "/likes/" + articleId + "/",

        {
            headers: {"X-CSRFToken": csrftoken},
        }
    );
    // Fetch likes
    fetch(request, {
        method: "GET",
        mode: "same-origin"
    }).then(res => res.json().then(json => {
        $('Button[name="like-button-' + articleId + '"').text('Likes: ' + json.likes);
    }));
}

// populates the comments for each article
async function populateComments() {
    let commentsContainers = $('.comments-container');
    for (let i = 0; i < commentsContainers.length; i++) {
        $('.comments-container').children().remove();
        await generateComments(commentsContainers[i]);
    }
}


// Generates the HTML for each comments section
async function generateComments(commentSection) {
    // Build request
    const request = new Request(
        "/comments/" + commentSection.title + "/",

        {
            headers: {"X-CSRFToken": csrftoken},
        }
    );
    // Fetch comments
    fetch(request, {
        method: "GET",
        mode: "same-origin"
    }).then(res => res.json().then(json => {
        if (json.message != "No comments found") {
            // Create html content
            // This html is structured so each chain of comments is within a comment-chain-container div, and each level of
            // comment depth is within a comment-level-container div, allowing for easy display of nested comments
            let comments = json.comments;
            contentToRender = "<div class='top-level-container'>"
            comments.forEach(generateCommentsChain)
            contentToRender += "</div>"
            commentSection.innerHTML = contentToRender;
        } else {
            console.log("comments don't exist");
        }
    }));
}

// Generates the chains of comments recursively
function generateCommentsChain(item) {
    contentToRender += "<div class='comment-chain-container'>"
    contentToRender += generateCommentHTML(item);
    if (item.children.length > 0) {
        contentToRender += "<div class='comment-level-container'>"
        item.children.forEach(generateCommentsChain)
        contentToRender += "</div>"
    }
    contentToRender += "</div>";
}

// Generate the actual html for each individual comment
function generateCommentHTML(comment) {
    let content = "<div class='comment'>"
    content += "<div class='comment-container' title='" + comment.id + "'>"
    content += "<p>" + comment.text + "</p>"
    content+="<p>Author: <a href='/profile/" + comment.author.id + "/' class='text-info'>" + comment.author.username + "</a> | Date created: " + new Date(comment.dateCreated).toLocaleString() + "</p>"
    if (comment.dateCreated < comment.dateUpdated) {
        content += "<p>Edited</p>"
    }
    content += "<button class='btn btn-dark' onclick='generateCommentReplyForm(" + comment.article + "," + comment.id + ")'>Reply</button>"
    if (user == comment.author.id) {
        content += "<button class='btn bg-dark text-light' onclick='deleteComment(" + comment.id + ")'>Delete Comment</button>"
        content += "<button class='btn bg-dark text-light' onClick='generateEditCommentForm(" + comment.id + ")'>Edit Comment</button>"
    }
    content += "</div>"
    content += "</div>"
    return content
}

// locates where to generate and provides details to generateCommentForm for generating a form for a reply
function generateCommentReplyForm(article, comment) {
    let commentContainer = $('.comment-container[title=' + comment + ']');
    let form = generateCommentForm(article, comment);
    commentContainer.append(form);
}

// locates where to generate and provides details to generateCommentForm for generating a form for a new comment
function generateNewCommentForm(article) {
    let commentsContainer = $('.comments-container[title=' + article + ']');
    let form = generateCommentForm(article, null);
    commentsContainer.prepend(form);
}

// generates an add comment form
function generateCommentForm(article, parent) {
    $("#newCommentForm").remove();
    let $form = $("<form id='newCommentForm'></form>");
    $form.append(
        "<div class='form-group'><label for='comment'>Comment:</label><textarea name='comment' class='form-control' rows='2' required ></textarea></div>"
    );
    $form.append(
        "<div class='form-group form-btns'><button name='add' class='btn btn-dark' onclick='addComment(" + article + "," + parent + ")'>Add</button><button name='cancel' class='btn btn-dark' onclick='cancelComment()'>Cancel</button></div>"
    );
    $form.submit(false);
    return $form;
}

// executes an add comment request
async function addComment(article, parent) {
    //construct form data
    let formData = $("#newCommentForm").serializeArray();
    if (
        formData[0].value == ""
    ) {
        // form validation as default form submit actions are prevented
        return;
    }
    let data = {
        'text': formData[0].value,
        'parent': parent,
    }
    //construct request
    const request = new Request(
        "/comments/" + article + "/",

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
    }).then(async function (response) {
        await populateComments();
    });
}

// executes a delete comment request
async function deleteComment(comment) {
    if (confirm("Are you sure you want to delete this comment?")) {
        //construct request
        const request = new Request(
            "/comments/edit/" + comment + "/",

            {
                headers: {"X-CSRFToken": csrftoken},
            }
        );
        //execute request
        fetch(request, {
            // execute fetch request
            method: "DELETE",
            mode: "same-origin",
        }).then(async function (response) {
            await populateComments();
        });
    }
}

// generates the form for editing a comment
function generateEditCommentForm(comment) {
    let commentContent = $('.comment-container[title=' + comment + ']').children('.comment-content');
    let currentContent = commentContent.children('span').text();
    commentContent.children('span').remove();
    $("#editCommentForm").remove();
    let $form = $("<form id='editCommentForm'></form>");
    $form.append(
        "<div class='form-group'><label for='comment'>Comment:</label><textarea name='comment' class='form-control' rows='2' required >" + currentContent + "</textarea></div>"
    );
    $form.append(
        "<div class='form-group form-btns'><button name='edit' class='btn btn-dark' onclick='editComment(" + comment + ")'>Edit</button><button name='cancel' class='btn btn-dark' onclick='cancelEdit(" + comment + ",\"" + currentContent + "\")'>Cancel</button></div>"
    );
    $form.submit(function (e) {
        // prevent form default action
        return false;
    });
    commentContent.append($form);
}

// executes an edit comment request
async function editComment(comment) {
    //construct form data
    let formData = $("#editCommentForm").serializeArray();
    if (
        formData[0].value == ""
    ) {
        // form validation as default form submit actions are prevented
        return;
    }
    let data = {
        'text': formData[0].value,
    }
    //construct request
    const request = new Request(
        "/comments/edit/" + comment + "/",

        {
            headers: {"X-CSRFToken": csrftoken},
        }
    );
    //execute request
    fetch(request, {
        // execute fetch request
        method: "PUT",
        mode: "same-origin",
        body: JSON.stringify(data),
    }).then(function (response) {
        populateComments();
    });


}

// cancels an edit and reverts comment back to previous content
function cancelEdit(comment, previousContent) {
    let commentContent = $(".comment-container[title=" + comment + "]").children(".comment-content");
    commentContent.children('form').remove();
    commentContent.append("<span>" + previousContent + "</span>");
}

// cancels a comment by removing the form
function cancelComment() {
    $("#newCommentForm").remove();
}

// handles the click of the likes button
async function handleLikesClick(articleId) {
    //construct request
    const request = new Request(
        "/likes/" + articleId + "/",

        {
            headers: {"X-CSRFToken": csrftoken},
        }
    )
    // Fetch likes
    fetch(request, {
        method: "POST",
        mode: "same-origin"
    }).then(res => res.json().then(json => {
        console.log(json.message);
        fetchLikes(articleId)
    }));
}

async function filterCategories(filter) {
    await populateInfo(filter);
}