const SPOTIFY_CLIENT_ID='3e0d8d7496fb4fbab87b68ec5d108fd7'
const SPOTIFY_CLIENT_SECRET='f7a4232895404a64b3b0cfdbe5bcb8e2'


var client_id = SPOTIFY_CLIENT_ID;
var client_secret = SPOTIFY_CLIENT_SECRET;
var redirect_uri = 'http://192.168.68.60:8000/callback';

const querystring = require('querystring');
const request = require('request');
const express = require('express')
const app = express()
const cors = require('cors')
const port = 8000

// add CORS
// app.use(cors());
// Configure CORS to allow requests from specific origin
app.use(cors({
  // origin: 'http://192.168.68.60:3000', 
  origin: 'http://localhost:3000', 
  methods: 'GET,POST,PUT,DELETE,OPTIONS',
  allowedHeaders: 'Content-Type, Authorization',
}));

app.get('/', function(req, res) {
  res.send({message: 'Hello World!'}); // Send a response to the client (e.g., 'Hello World!')
})
var stateKey = 'spotify_auth_state';
app.get('/callback', function(req, res) {
  var code = req.query.code || null;
  var state = req.query.state || null;
  console.log("req.query",req.query);
  // res.send('Callback');

  res.clearCookie(stateKey);
    var authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      form: {
        code: code,
        redirect_uri: redirect_uri,
        grant_type: 'authorization_code'
      },
      headers: {
        'content-type': 'application/x-www-form-urlencoded',
        Authorization: 'Basic ' + (new Buffer.from(client_id + ':' + client_secret).toString('base64'))
      },
      json: true
    };

    request.post(authOptions, function(error, response, body) {
      if (!error && response.statusCode === 200) {

        var access_token = body.access_token,
            refresh_token = body.refresh_token;

        console.log('access_token',access_token);
        console.log('refresh_token',refresh_token);

        var options = {
          url: 'https://api.spotify.com/v1/me',
          headers: { 'Authorization': 'Bearer ' + access_token },
          json: true
        };

        // use the access token to access the Spotify Web API
        request.get(options, function(error, response, body) {
          console.log(body);
        });

        // we can also pass the token to the browser to make requests from there
        res.redirect('/#' +
          querystring.stringify({
            access_token: access_token,
            refresh_token: refresh_token
          }));
      } else {
        res.redirect('/#' +
          querystring.stringify({
            error: 'invalid_token'
          }));
      }
    });
  
})

function generateRandomString(length) {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (var i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}


app.get('/login', async function(req, res) {

  var state = generateRandomString(16);
  var scope = 'user-read-private user-read-email';

  console.log('client_id: ' + client_id);
  console.log('redirect_uri: ' + redirect_uri);

  // const response = await fetch('https://accounts.spotify.com/authorize?' +
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));
  
  // res.send(response);
});


app.listen(port, () => console.log(`App listening on port ${port}!`))