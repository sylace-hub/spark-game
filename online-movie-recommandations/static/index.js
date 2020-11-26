function addRating() {
    var tableBody = document.getElementById("ratings-table-body");

    var index = tableBody.getElementsByTagName('tr').length;
    var row = tableBody.insertRow(index);
    row.setAttribute("id", index);

    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);

    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("class", "form-control");
    input.setAttribute("placeholder", "Movie Identifier");
    input.setAttribute("name", "movieId_" + index);

    var select = document.createElement("select");
    select.setAttribute("class", "form-control")
    select.setAttribute("name", "rating_" + index);

    var i;
    for (i = 1; i <= 5; i++) {
        var option = document.createElement("option");
        option.setAttribute("value", i);
        var node = document.createTextNode(i);
        option.appendChild(node);
        select.appendChild(option);
    }

    cell1.appendChild(input);
    cell2.appendChild(select);
}

function addMovieRecommendation(value, index, array) {
    var table = document.getElementById("movies-table");
    var tableBody = document.getElementById("movies-table-body");
    var row = tableBody.insertRow(index);

    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);

    cell1.innerHTML = index + 1;
    cell2.innerHTML = value.title;
}

function isValidForm(firstParam, secondParam) {
    if (firstParam === "" || isNaN(firstParam)) {
        return false;
    }
    if (secondParam === "" || isNaN(secondParam)) {
        return false;
    }
    return true;
}

function submitRatings(userId) {
    if (userId === "" || isNaN(userId)) {
        alert("User Identifier must be a numerical value.");
    } else {
        console.log("Add new ratings to the model for user " + userId);

        document.getElementById("add-ratings-btn").disabled = true;
        document.getElementById("add-rating-line-btn").disabled = true;
        
        var ratingsForm = document.getElementById("ratings-form");
        var data = new FormData(ratingsForm);

        var xhr = new XMLHttpRequest();
        var url = "http://localhost:5432/" + userId + "/newratings";
        xhr.open("POST", url, true);
        xhr.onload = function () {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    var tableBody = document.getElementById("ratings-table-body");
                    while (tableBody.hasChildNodes()) {
                        tableBody.removeChild(tableBody.firstChild);
                    }
                    addRating();
                    alert(this.responseText);
                }

                if (this.status == 500) {
                    alert(this.response.substring(this.response.indexOf("<p>") + 3, this.response.indexOf("</p>")))
                }

                document.getElementById("add-ratings-btn").disabled = false;
                document.getElementById("add-rating-line-btn").disabled = false;
            }
        };
        xhr.send(data);
    }
}

function predictRating(userId, movieId) {
    if (isValidForm(userId, movieId)) {
        console.log("Predict rating for movie " + movieId + " and user " + userId);
        
        document.getElementById("get-prediction-btn").disabled = true;
        document.getElementById("predited-rating-result").innerHTML = "Processing...";

        var xmlhttp = new XMLHttpRequest();
        var url = "http://localhost:5432/" + userId + "/ratings/" + movieId;

        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    var rating = parseFloat(this.response).toFixed(2);
                    var message = "The prediction failed, movie not found for the given identifier."
                    if (rating != -1) {
                        message = "Predicted rating for<br> movie " + movieId + " and user " + userId + " is :<br>" + rating;
                    }
                    document.getElementById("predited-rating-result").innerHTML = message;
                }

                document.getElementById("get-prediction-btn").disabled = false;
            }
        };

        xmlhttp.open("GET", url, true);
        xmlhttp.responseType = 'json';
        xmlhttp.send();
    } else {
        alert("User Identifier and Movie Identifier must be numerical values.");
    }
}

function getRecommendations(userId, nbMovies) {
    if (isValidForm(userId, nbMovies) && nbMovies > 0) {
        console.log("Get top " + nbMovies + " movies for user " + userId);
        document.getElementById("get-recommendations-btn").disabled = true;

        var xmlhttp = new XMLHttpRequest();
        var url = "http://localhost:5432/" + userId + "/ratings/top/" + nbMovies;

        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    var tableBody = document.getElementById("movies-table-body");
                    while (tableBody.hasChildNodes()) {
                        tableBody.removeChild(tableBody.firstChild);
                    }

                    var result = this.response;
                    result.forEach(addMovieRecommendation);
                }

                document.getElementById("get-recommendations-btn").disabled = false;
            }
        };

        xmlhttp.open("GET", url, true);
        xmlhttp.responseType = 'json';
        xmlhttp.send();
    } else {
        alert("User Identifier and Number of movies must be numerical values.");
    }
}