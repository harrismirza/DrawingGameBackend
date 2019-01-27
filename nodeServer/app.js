global.atob = require("atob");

const express = require('express')
const sketchjs = require('./sketch.js')
const bodyParser = require('body-parser')
const app = express()
const port = 3005

app.use(bodyParser.json());

app.use(express.static('./models'))

app.post("/", async (req, resp) => {
    console.log("Got Request");
    console.log(req.body);

    category = req.body.category;
    lines = req.body.lines;

    console.log(category);
    console.log(lines);

    strokes = await sketchjs.sketch(category, lines);

    resp.send(strokes);
})

app.listen(port, '0.0.0.0')