require('es6-promise').polyfill();
require('isomorphic-fetch');
require('@tensorflow/tfjs-node')
ms = require("@magenta/sketch");

function atob(str) {
  return Buffer.from(str, 'base64').toString('binary');
}

async function sketch(category, lines) {
    // Available SketchRNN models.
    const BASE_URL = 'http://localhost:3005/';
    let model;

    // Model state.
    let modelState; // Store the hidden states of rnn's neurons.
    let temperature = Number.MIN_VALUE; // Controls the amount of uncertainty of the model.
    let modelLoaded = false;

    let dx, dy; // Offsets of the pen strokes, in pixels.
    let x, y; // Absolute coordinates on the screen of where the pen is.
    let pen = [0, 0, 0]; // Current pen state, [pen_down, pen_up, pen_end].
    let previousPen = [1, 0, 0]; // Previous pen state.
    const PEN = {DOWN: 0, UP: 1, END: 2};

    async function initModel(category) {
        modelLoaded = false;
        if (model) {
            model.dispose();
        }

        model = new ms.SketchRNN(`${BASE_URL}${category}.gen.json`);
        console.log("Created Model");

        await model.initialize();

        modelLoaded = true;
        console.log('SketchRNN model loaded.');

        // Initialize the scale factor for the model. Bigger -> large outputs
        model.setPixelFactor(10);
        console.log("Bias: " + model.lstmBias);
        console.log("Num Units: " + model.numUnits);
    };

    async function completeDrawing(initial_strokes, lastx, lasty) {
        console.log("Completing Drawing");
        strokes = initial_strokes.slice()

        // Load current strokes into model
        let newState = model.zeroState();
        console.log("Got Zero State");
        let zeroInput = model.zeroInput();
        console.log("Got Zero Input");
        newState = model.update(zeroInput, newState)
        console.log("Added Zero Input to State");
        console.log("Adding Strokes");
        console.log("Strokes");
        newState = model.updateStrokes(strokes, newState);
        console.log("Updated State");

        modelState = model.copyState(newState);

        x = lastx;
        y = lasty;
        previousPen = [0, 1, 0];
        while(!(previousPen[PEN.END] === 1)){
            const pdf = model.getPDF(modelState, temperature);
            [dx, dy, ...pen] = model.sample(pdf);
            strokes.push([dx, dy, ...pen]);

            x += dx;
            y += dy;
            previousPen = pen;
            modelState = model.update([dx, dy, ...pen], modelState);
        }
        console.log("Generated Strokes");

        return strokes;
    }

    function strokesToLines(strokes, startingX, startingY)
    {
        var lines = [];
        var line = [];
        var x = startingX;
        var y = startingY;
        penDown = true
        for(i=0; i < strokes.length; i ++)
        {
            x = x + strokes[i][0];
            y = y + strokes[i][1];
            if(penDown)
            {
                line.push([x, y]);
            }else{
                lines.push(line);
                line = []
            }

            if(strokes[i][2] === 1){
                penDown = true;
            }else if(strokes[i][3] === 1)
            {
                penDown = false;
            }else{
                return lines
            }
        }
    }

    console.log("Defined methods");
    await initModel(category);
    console.log("Initialised Model");
    // Convert lines to strokes
    simple_lines = model.simplifyLines(lines);
    strokes = model.linesToStroke(simple_lines);
    strokes[strokes.length-2][3] = 0
    strokes[strokes.length-2][2] = 1
    strokes[strokes.length-1][4] = 0
    strokes[strokes.length-1][3] = 1
    console.log("Converted Lines");

    last_line = lines[lines.length-1];
    last_coord = last_line[last_line.length-1];

    return strokesToLines(await completeDrawing(strokes, last_coord[0], last_coord[1]), lines[0][0][0], lines[0][0][1]);

};

module.exports = {sketch}
