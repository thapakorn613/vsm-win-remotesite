//include required modules

const jwt = require("jsonwebtoken");
const config = require("./config");
const rp = require("request-promise");
var path = require("path");

const express = require("express");
const app = express();

const edge = require("windows-edge");
//get the form

// app.get("/", (req, res) => res.render('index'));

// use userinfo from the form and make a post request to /userinfo
app.get("/", (req, res) => {
  //store the email address of the user in the email variable
  //   email = req.body.email;
  email = "thapakorn613@gmail.com";
  //check if the email was stored in the console
  console.log("start zoom ");
  //Store the options for Zoom API which will be used to make an API call later.
  var options = {
    //You can use a different uri if you're making an API call to a different Zoom endpoint.
    uri: "https://api.zoom.us/v2/users/" + email,
    qs: {
      status: "inactive"
    },
    auth: {
      bearer: token
    },
    json: true //Parse the JSON string in the response
  };

  //Use request-promise module's .then() method to make request calls.
  rp(options)
    .then(function(response) {
      //printing the response on the console
      linkZoomId = response.personal_meeting_url;
      console.log("linkZoomId", linkZoomId);
      //console.log("User has", response);
      resp = response;
      //Adding html to the page
      var title1 = "<center><h3>Your token: </h3></center>";
      var result1 =
        title1 +
        '<code><pre style="background-color:#aef8f9;">' +
        token +
        "</pre></code>";
      var title = "<center><h3>User's information:</h3></center>";
      //Prettify the JSON format using pre tag and JSON.stringify
      var result =
        title +
        '<code><pre style="background-color:#aef8f9;">' +
        JSON.stringify(resp, null, 2) +
        "</pre></code>";
      res.send(result1 + "<br>" + result);

      edge({ uri: linkZoomId }, (err, ps) => {
        if (err) throw err;
        ps.on("error", console.error);
        ps.on("exit", code => {
          // Browser exited
        });
        setTimeout(() => {
          ps.kill();
        }, 3000);
      });
    })
    .catch(function(err) {
      // API call failed...
      console.log("API call failed, reason ", err);
    });
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`));

// setTimeout(() => {
//     process.kill(process.pid, 'SIGTERM')
// }, 3000);


// process.on('SIGTERM', () => {
//     server.close(() => {
//         console.log('Process terminated')
//     })
// })
