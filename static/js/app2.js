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

  // var imgFilenames = d3.select("#imgResponse").text().trim();
  // imgFilenames = JSON.parse(imgFilenames);
  // console.log(imgFilenames);

  // imgFilenames.forEach(function (d) {
  //   var filename = d;
  //   console.log(filename);
  //   //   d3.select("#imgResponse")
  //   //     .html(() => {
  //   //       return `<img src="static/detections/${filename}>`;
  //   //   });
  // });


  // console.log(imgFilenames);

  // var dropzone = document.getElementById("dropzone");
  // var show_resultss = document.getElementById("show_results");
  // var get_result = document.getElementById("get_result");
  // var recorderr = document.getElementById("recorderr");
  // var icon_options = document.getElementById("icon_options");
  // var imgResponse = document.getElementById("imgResponse");
  //var data = ["cups", "spoon", "knife"];

  // function image_up() {
  //   // $("#icon_options").replaceWith(icon_optionsclone.clone());
  //   // $("#recorderr").empty();
  //   icon_options.style.display = "block";
  //   recorderr.style.display = "none";
  //   show_resultss.style.display = "block";
  //   imgResponse.style.display = "block";
  //   d3.select("#text_for_icon").text("UPLOAD IMAGE");
  // }

  // function video_up() {
  //   // $("#icon_options").replaceWith(icon_optionsclone.clone());
  //   // $("#recorderr").empty();
  //   icon_options.style.display = "block";
  //   recorderr.style.display = "none";
  //   //show_results.style.display = "block";
  //   d3.select("#text_for_icon").text("UPLOAD VIDEO");
  //   show_resultss.style.display = "block";
  //   imgResponse.style.display = "block";
  // }

  // function show_results() {
  //   show_resultss.style.display = "block";
  //   imgResponse.style.display = "block";
  // }

  // function video_stream() {
  //   //recorderr.disabled = false;
  //   // $("#recorderr").replaceWith(recorderrclone.clone());
  //   // $("#icon_options").empty();
  //   recorderr.style.display = "block";
  //   icon_options.style.display = "none";
  //   show_resultss.style.display = "none";
  //   imgResponse.style.display = "none";
  // }

  function init() {
    // image_up();
    drawTable();
    buildTable(buildTable(Object.keys(scrapeddata)[0], "best_match"));
  }

  d3.select("#image_up").on("click", image_up);
  d3.select("#video_up").on("click", video_up);
  d3.select("#video_stream").on("click", video_stream);
  //d3.select("#show_results").on("click", show_results);

  // var object = Object.keys(scrapeddata)[0];
  // var filter = "best_match";

  init();

  function drawTable() {

    var values = [classesArray.map(function (x) { return x.toUpperCase() }), confidencesArray,];

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

  console.log(scrapeddata);

  // function optionChangedOne(newObject) {
  //   object = newObject;
  //   filter = "best_match";
  //   d3.select("#my-table")
  //     .select("tbody").html("");
  //     buildTable();
  // }

  // function optionChangedTwo() {
  //   filter = d3.select("#selDatasetTwo").property("value");;
  //   d3.select("#my-table")
  //     .select("tbody").html("");
  //   object = d3.select("#selDatasetOne").property("value");
  //   console.log(value);
  //   buildTable();
  // }
  // On change to the DOM, call getData()
  // d3.select("#selDatasetOne").on("change", buildTable(getvalue("#selDatasetOne"), 'best_match'));
  // d3.select("#selDatasetTwo").on("change", buildTable(getvalue("#selDatasetOne"), getvalue("#selDatasetTwo")));

  // Function called by DOM changes
  function getvalue(sel) {

    var dropdownMenu = d3.select(sel);
    // Assign the value of the dropdown menu option to a variable
    var value = dropdownMenu.property("value");

    return value

  };

  var sel1 = document.getElementById('selDatasetOne');
  var sel2 = document.getElementById('selDatasetTwo');


  function getSelectedOption(sel) {
    var opt;
    for (var i = 0, len = sel.options.length; i < len; i++) {
      opt = sel.options[i];
      if (opt.selected === true) {
        break;
      }
    }
    return opt;
  }

  // assign onclick handlers to the buttons
  // sel1.onclick = function () {
  //   d3.select("#my-table")
  //     .select("tbody").html("");
  //   buildTable(getSelectedOption(sel1), 'best_match');
  // }

  // sel2.onclick = function () {
  //   d3.select("#my-table")
  //     .select("tbody").html("");
  //   buildTable(getSelectedOption(sel1), getSelectedOption(sel2));
  // }

  function buildTable(object, filter) {
    //var firstkey = Object.keys(scrapeddata)[0]
    // var sel = document.getElementById('selDatasetOne');
    // if (typeof (filter) == 'undefined') {
    //   console.log(sel.value);
    // }

    var data = scrapeddata[object][filter];
    var products_name = data["products_name"];
    var prices = data["prices"];
    var ratings = data["ratings"];
    var no_of_reviews = data["no_of_reviews"];
    var products_url = data["products_url"];
    var products_img = data["products_img"];
    var delivery_info = data["delivery_info"];

    new_data = [];
    for (var i = 0; i < products_name.length; i++) {
      new_data.push({
        "products_name": products_name[i], "prices": prices[i], "ratings": ratings[i],
        "no_of_reviews": no_of_reviews[i], "products_url": products_url[i],
        "products_img": products_img[i], "delivery_info": delivery_info[i]
      })
    };

    console.log(new_data);


    d3.select("#my-table")
      .select("tbody")
      .selectAll("tr")
      .data(new_data)
      .enter()
      .append("tr")
      .html(function (d) {
        return `<td><img style="height:100px, width:100px" src=${d.products_img}></td>
              <td><a href=${d.products_url}>${d.products_name}</a></td>
              <td>${d.prices}</td>
              <td>${d.ratings}</td>
              <td>${d.no_of_reviews}</td>
              <td>${d.delivery_info}</td>`;
      });
  };;

