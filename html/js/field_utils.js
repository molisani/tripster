function $_GET(k) {
    return decodeURI((RegExp(k+'='+'(.+?)(&|$)').exec(location.search)||[,null])[1]);
}

function formData(formID) {
    data = {};
    formArray = $(formID).serializeArray();
    for (var i = 0; i < formArray.length; i++) {
        data[formArray[i]["name"]] = formArray[i]["value"]
    }
    return data;
}
