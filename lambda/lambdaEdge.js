'use strict';
exports.handler = (event, context, callback) => {

    // Extract the request from the CloudFront event that is sent to Lambda@Edge
    var request = event.Records[0].cf.request;

    // Extract the URI from the request
    var olduri = request.uri;

    //ignore the serial number on the end of the path
    var serialNumberValidation=/^[0-9a-z]{12}$/;
    var elements = olduri.split("/");
    var last_element = elements.pop();
    if ( last_element.match(serialNumberValidation)) {
        var newuri = elements.join("/")+"/index.html";
    }
    else {
        var newuri = olduri;
    }

    // Match any '/' that occurs at the end of a URI. Replace it with a default index
    newuri = newuri.replace(/\/$/, '\/index.html');

    // Replace the received URI with the URI that includes the index page
    request.uri = newuri;

    // Return to CloudFront
    return callback(null, request);

};