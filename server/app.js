const SPOTIFY_CLIENT_ID='3e0d8d7496fb4fbab87b68ec5d108fd7'
const SPOTIFY_CLIENT_SECRET='f7a4232895404a64b3b0cfdbe5bcb8e2'
const port = 8000

var express = require('express');
var request = require('request');
var crypto = require('crypto');
var cors = require('cors');
var querystring = require('querystring');
var cookieParser = require('cookie-parser');

var client_id = '3e0d8d7496fb4fbab87b68ec5d108fd7'; // your clientId
var client_secret = 'f7a4232895404a64b3b0cfdbe5bcb8e2'; // Your secret
var redirect_uri = 'http://localhost:8000/callback'; // Your redirect uri

const generateRandomString = (length) => {
  return crypto
  .randomBytes(60)
  .toString('hex')
  .slice(0, length);
}

var stateKey = 'spotify_auth_state';

var app = express();

// add CORS
app.use(cors());
// Configure CORS to allow requests from specific origin
// app.use(cors({
//   // origin: 'http://192.168.68.60:3000', 
//   origin: 'http://localhost:3000', 
//   methods: 'GET,POST,PUT,DELETE,OPTIONS',
//   allowedHeaders: 'Content-Type, Authorization',
// }));

app.get('/', function(req, res) {
  res.send({message: 'Hello World!'}); // Send a response to the client (e.g., 'Hello World!')
})


app.get('/login', async function(req, res) {

  var state = generateRandomString(16);
  res.cookie(stateKey, state);

  // your application requests authorization
  var scope = 'user-read-private user-read-email';


  // // const response = await fetch('https://accounts.spotify.com/authorize?response_type=code&client_id=' + client_id + '&scope=' + scope + '&redirect_uri=' + redirect_uri + '&state=' + state)
  // const response = request.get({
  //   url: 'https://accounts.spotify.com/authorize?response_type=code&client_id=' + client_id + '&scope=' + scope + '&redirect_uri=' + redirect_uri + '&state=' + state
  // }, function (error, response, body) {
  //   console.log('error:', error); // Print the error if one occurred
  //   console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
  //   console.log('body:', body); // Print the HTML for the Google homepage.
  //   console.log('response:', response)
  // })

  // console.log(response)

  // const data = await response.json()
  // console.log(data)

  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));
});

app.get('/callback', function(req, res) {

  // your application requests refresh and access tokens
  // after checking the state parameter

  var code = req.query.code || null;
  var state = req.query.state || null;
  var storedState = req.cookies ? req.cookies[stateKey] : null;

  if (state === null || state !== storedState) {
    res.redirect('/#' +
      querystring.stringify({
        error: 'state_mismatch'
      }));
  } else {
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
  }
});

const DEFAULT_MUSIC_GENRES = [
  { genre: "Rock", subgenres: ["Alternative", "Classic Rock", "Hard Rock"] },
  { genre: "Pop", subgenres: ["Dance", "Synthpop", "Electropop"] },
  { genre: "Jazz", subgenres: ["Smooth", "Bebop", "Swing"] },
  { genre: "Classical", subgenres: ["Baroque", "Romantic", "Classical Era"] },
  { genre: "Electronic", subgenres: ["House", "Techno", "Trance"] },
  { genre: "Country", subgenres: ["Bluegrass", "Honky Tonk", "Country Rock"] },
  { genre: "Rap", subgenres: ["Trap", "Old School", "Gangsta Rap"] },
  { genre: "R&B", subgenres: ["Soul", "Contemporary R&B", "Funk"] },
  { genre: "Latin", subgenres: ["Reggaeton", "Salsa", "Bossa Nova"] },
];
app.get('/user/music/genres', async function(req, res) {

  res.send(DEFAULT_MUSIC_GENRES);
})

app.listen(port, () => console.log(`App listening on port ${port}!`))