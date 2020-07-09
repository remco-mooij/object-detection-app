// var detectionResults = d3.select("#detResponse").text().trim();
// // namesTrimmed = names.trim();
// // console.log(namesTrimmed);

var allowable_items = ['bicycle', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'baseball bat', 'baseball glove', 'skateboard',
  'surfboard', 'tennis racketbottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', ' banana', 'apple',
  'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cakechair', 'sofa', 'pottedplant',
  'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
  'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', ' scissors', ' teddy bear', 'hair drier', 'toothbrush'];
// detectionResults = detectionResults.replace(/'/g, '"');

// detectionResults = JSON.parse(detectionResults);
classesArray = parsed.detections.map(x => x.class)
console.log(classesArray);

confidencesArray = parsed.detections.map(x => x.confidence)
console.log(confidencesArray);

// detections = JSON.parse('{{response | tojson}}');
// console.log(detections);

classesArray.forEach((data) => {
  if (allowable_items.some(f => f === data)) {
    var drop = d3.select("#selDatasetOne").append("option");
    drop.text(data.toUpperCase());
    drop.property("value", data);
  }
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
  show_results.style.display = "block";
  d3.select("#text_for_icon").text("UPLOAD IMAGE");
}

function video_up() {
  // $("#icon_options").replaceWith(icon_optionsclone.clone());
  // $("#recorderr").empty();
  icon_options.style.display = "block";
  recorderr.style.display = "none";
  show_results.style.display = "block";
  d3.select("#text_for_icon").text("UPLOAD VIDEO");
}

function video_stream() {
  //recorderr.disabled = false;
  // $("#recorderr").replaceWith(recorderrclone.clone());
  // $("#icon_options").empty();
  recorderr.style.display = "block";
  icon_options.style.display = "none";
  show_results.style.display = "none";
}

function init() {
  image_up();
  drawTable();
  buildTable("bicycle", "best_match")
}

d3.select("#image_up").on("click", image_up);
d3.select("#video_up").on("click", video_up);
d3.select("#video_stream").on("click", video_stream);

init();

function drawTable() {

  var values = [classesArray.map(function (x) { return x.toUpperCase() }),confidencesArray,];

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
          color: "#677F9F",
        },
        font: {
          family: "'Barlow Condensed' , 'sans-serif'",
          size: 20,
          color: "white",
        },
      },

      cells: {
        values: values,
        align: ["center", "center"],
        height: 50,
        width: 100,
        line: {
          color: "#506784",
          width: 1,
        },
        fill: {
          color: ["#B8C4D2", "#BCC8D6"],
        },
        font: {
          family: "'Barlow Condensed' , 'sans-serif'",
          size: 18,
          color: "white",
        },
      },
    },
  ];

  var layout = {
    // title: `<b>DETECTIONS DATA </b>`,
    autosize: false,
    width: $(window).width() * 0.8,
    height: 200,
    margin: {
      l: 3,
      r: 3,
      b: 3,
      t: 3,
    },
    plot_bgcolor: "#FFFFFF",
    paper_bgcolor: "#FFFFFF",
  };

  Plotly.newPlot("table", data, layout, { responsive: true });
}

//$("#recorderr").find("*").prop("disabled", true);

window.onresize = function () {
  drawTable();
};



// function optionChangedOne(newYear) {
//   year = newYear;
//   buildPanel();
//   d3.select('#scatter').html("");
//   d3.select('#cloud').html(""),
//     d3.select('#linearGauge').html(""),
//     buildCharts(newYear);
//   buildScatter();
//   drawCloud();
//   drawLinearGauge();
// }

// function optionChangedTwo(newCountry) {
//   country = newCountry;
//   buildPanel();
//   drawBar();
// }

function buildTable(object,filter) {
  //var firstkey = Object.keys(scrapeddata)[0]
  var data = scrapeddata[object][filter];
  var products_name = data["products_name"];
  var price = data["price"];
  var ratings = data["ratings"];
  var no_of_reviews = data["no_of_reviews"];
  var products_url = data["products_url"];
  var products_img = data["products_img"];
  var delivery_info = data["delivery_info"];
  
  var myTableDiv = document.getElementById("my-table");
  for (var i = 0; i < products_name.length; i++) {
    d3.select("#my-table")
      .select("tbody")
      .selectAll("tr")
      .data(data)
      .enter()
      .append("tr")
      .html(`<td>${products_name[i]}</td><td>${price[i]}</td>
            <td>${ratings[i]}</td><td>${no_of_reviews[i]}</td>
            <td>${products_img[i]}</td><td>${delivery_info[i]}</td>`)
  };
};