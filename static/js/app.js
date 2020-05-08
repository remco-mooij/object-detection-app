var detectionResults = d3.select("#detResponse").text().trim();
// namesTrimmed = names.trim();
// console.log(namesTrimmed);


detectionResults = detectionResults.replace(/'/g, '"');

detectionResults = JSON.parse(detectionResults);
classesArray = detectionResults.detections.map(x => x.class)
console.log(classesArray);

confidencesArray = detectionResults.detections.map(x => x.confidence)
console.log(confidencesArray);

// detections = JSON.parse('{{response | tojson}}');
// console.log(detections);

classesArray.forEach((data) => {
  var drop = d3.select("#selDataset").append("option");
  drop.text(data.toUpperCase());
  drop.property("value", data);
});

var imgFilenames = d3.select("#imgResponse").text().trim();
imgFilenames = JSON.parse(imgFilenames);
console.log(imgFilenames);

imgFilenames.forEach(function(d) {
  var filename = d;
  console.log(filename);
//   d3.select("#imgResponse")
//     .html(() => {
//       return `<img src="static/detections/${filename}>`;
//   });
});


// console.log(imgFilenames);

var dropzone = document.getElementById("dropzone");
var recorderr = document.getElementById("recorderr");
var icon_options = document.getElementById("icon_options");
var data = ["cups", "spoon", "knife"];

function image_up() {
  // $("#icon_options").replaceWith(icon_optionsclone.clone());
  // $("#recorderr").empty();
  icon_options.style.display = "block";
  recorderr.style.display = "none";
  d3.select("#text_for_icon").text("UPLOAD IMAGE");
}

function video_up() {
  // $("#icon_options").replaceWith(icon_optionsclone.clone());
  // $("#recorderr").empty();
  icon_options.style.display = "block";
  recorderr.style.display = "none";
  d3.select("#text_for_icon").text("UPLOAD VIDEO");
}

function video_stream() {
  //recorderr.disabled = false;
  // $("#recorderr").replaceWith(recorderrclone.clone());
  // $("#icon_options").empty();
  recorderr.style.display = "block";
  icon_options.style.display = "none";
}

function init() {
  image_up();
  drawTable();
}

d3.select("#image_up").on("click", image_up);
d3.select("#video_up").on("click", video_up);
d3.select("#video_stream").on("click", video_stream);

init();

function drawTable() {

  var values = [classesArray,confidencesArray,];

  var data = [
    {
      type: "table",
      columnorder: [1, 2],
      columnwidth: [200, 200],

      header: {
        values: [["<br>CLASSES</br>"], ["<br>CONFIDENCE</br>"]],
        align: ["center", "center"],
        height: 40,
        line: {
          width: 1,
          color: "#506784",
        },
        fill: {
          color: "rgb(65, 130, 190)",
        },
        font: {
          family: "'Barlow Condensed' , 'sans-serif'",
          size: 17,
          color: "white",
        },
      },

      cells: {
        values: values,
        align: ["left", "center"],
        height: 50,
        width: 100,
        line: {
          color: "#506784",
          width: 1,
        },
        fill: {
          color: ["rgba(65, 130, 190, .5)", "white"],
        },
        font: {
          family: "'Barlow Condensed' , 'sans-serif'",
          size: 15,
        },
      },
    },
  ];

  var layout = {
    title: `<b>DETECTIONS DATA </b>`,
    // autosize: false,
    width: 600,
    height: 500,
    margin: {
      l: 50,
      r: 50,
      b: 100,
      t: 100,
    },
    plot_bgcolor: "#FFFFFF",
    paper_bgcolor: "#FFFFFF",
  };

  Plotly.newPlot("table", data, { responsive: true });
}

//$("#recorderr").find("*").prop("disabled", true);





