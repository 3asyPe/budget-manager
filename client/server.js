// function requireHTTPS(req, res, next) {
//     // The 'x-forwarded-proto' check is for Heroku
//     if (!req.secure && req.get('x-forwarded-proto') !== 'https') {
//         return res.redirect('https://' + req.get('host') + req.url);
//     }
//     next();
// }
const express = require('express');
const app = express();
const port = process.env.PORT || 8080;
// app.use(requireHTTPS);

app.use(express.static('./dist/client'))

app.get(`/*`, function(req, res) {
    console.log(req)
    console.log(res)
    res.sendFile(`index.html`, {root: './dist/client'}
  );
});

app.listen(port, () => {
    console.log("Server is listening on port "+port);
});
