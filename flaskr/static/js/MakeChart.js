function makeChart(agg_emotions)
{
  emotion_axes = [
    []
  ]
  sentiment_axes = []

  emotion_sum = 0.0
  sentiment_sum = 0.0
  maxPercent = -1;

  for (key in agg_emotions) {
    if (agg_emotions.hasOwnProperty(key) && key !== 'positive' && key !== 'negative') {
      emotion_sum += agg_emotions[key]
    } else if (key === 'positive' || key === 'negative') {
      sentiment_sum += agg_emotions[key]
    }
  }

  for (key in agg_emotions) {
    if (agg_emotions.hasOwnProperty(key) && key !== 'positive' && key !== 'negative') {

      percent = agg_emotions[key] / emotion_sum;

      if (maxPercent < percent) {
        maxPercent = percent
      }

      emotion_axes[0].push({
        "axis": key,
        value: percent
      })
    } else if (key === 'positive' || key === 'negative') {
      sentiment_axes.push({
        "axis": key,
        value: (agg_emotions[key] / sentiment_sum) * 100
      })
    }
  }

  var margin = {
      top: 100,
      right: 100,
      bottom: 100,
      left: 100
    },
    width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
    height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);

  var color = d3.scale.ordinal()
    .range(["#EDC951", "#CC333F", "#00A0B0"]);

  var radarChartOptions = {
    w: width,
    h: height,
    margin: margin,
    maxValue: Math.trunc(maxPercent + .01),
    levels: 5,
    roundStrokes: true,
    color: color
  };

  RadarChart("#emotion-chart", emotion_axes, radarChartOptions)

  // set the dimensions and margins of the graph
  var margin = {
      top: 30,
      right: 30,
      bottom: 70,
      left: 60
    },
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

  // append the svg object to the body of the page
  var svg = d3.select("#sentiment-chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");

  var x = d3.scaleBand()
    .range([0, width])
    .domain(sentiment_axes.map(function(d) {
      return d.axis;
    }))
    .padding(0.2);

  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");

  // Add Y axis
  var y = d3.scaleLinear()
    .domain([0, 100])
    .range([height, 0]);
  svg.append("g")
    .call(d3.axisLeft(y));

  // Bars
  svg.selectAll("mybar")
    .data(sentiment_axes)
    .enter()
    .append("rect")
    .attr("x", function(d) {
      return x(d.axis);
    })
    .attr("y", function(d) {
      return y(d.value);
    })
    .attr("width", x.bandwidth())
    .attr("height", function(d) {
      return height - y(d.value);
    })
    .attr("fill", "#69b3a2")
}
