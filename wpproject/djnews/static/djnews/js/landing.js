const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value; // get csrftoken from DOM
let contentToRender;
$(document).ready(function () {
    // The following function fetches and generates the comments of each displayed article
    $('.comments-container').each(async function (i, obj) {
        // Build request
        const request = new Request(
            "/comments/" + obj.title + "/",

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
                obj.innerHTML = contentToRender;
            } else {
                console.log("comments don't exist");
            }
        }));
    });
});

// Generates the chains of comments recursively
function generateCommentsChain(item, index) {
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
    // let content = "<p>id: "+comment.id +" parent: " + comment.parent + " text: " + comment.text+"</p>"
    let content = "<div class='comment'>"
    content += "<div class='comment-content'>"
    content += "<div>" + comment.text + "</div><div>Date created: " + comment.dateCreated + "</div>"
    if (comment.dateCreated < comment.dateUpdated) {
        content += "<div>Edited</div>"
    }
    content += "</div>"
    content += "</div>"
    return content
}

function generateNewCommentForm(articleId) {
    let commentsContainer = $('.comments-container[title=' + articleId + ']');
    let form = generateCommentForm(articleId, null);
    commentsContainer.prepend(form);
}

function generateCommentForm(articleId, parent) {
    $("#newCommentForm").remove();
    let $form = $("<form id='newCommentForm'></form>");
    $form.append(
        '<div class="form-group"><label for="comment">Comment:</label><textarea name="comment" class="form-control" rows="2" required ></textarea></div>'
    );
    $form.append(
        '<div class="form-group form-btns"><button name="add" class="btn btn-dark" onclick="addComment()">Add</button></div>'
    );
    $form.submit(function (e) {
        // prevent form default action
        return false;
    });
    return $form;
}

function addComment() {
    let formData = $("#newCommentForm").serializeArray();
    $("#newCommentForm").remove();
    console.log(formData);
}