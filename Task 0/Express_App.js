var express = require('express');
var app = express();
const cors = require('cors');
var db = require('./Database.js');
// express app
app.use(express.json());
app.use(cors());
//  var variable = JSON.parse(variable)

// Server port
var HTTP_PORT = 80;
// Start server
//,'192.168.1.3'
app.listen(HTTP_PORT, () => {
  console.log("Server running on port %PORT%".replace("%PORT%", HTTP_PORT));
});

// Root endpoint
app.get("/", (req, res, next) => {
    res.json({ message: "" });
  });
  
  // Insert here other API endpoints

  app.post("/Sensors/", (req, res, next) => {
    var errors = []; // error array
    // console.log(req.body)
    if (!req.body.reeding) {
      errors.push("No reading sent");
    }
    var SensorData = {
      Temperature: req.body.Temperature,
      // Humidity: parseInt(req.body.Humidity),
      Time: new Date().getTime(),
    };
    console.log(SensorData)
    var sql = "INSERT INTO Sensors (Temperature,Humidity,Time) VALUES (?,?,?)";
    var parameters = [SensorData.Temperature,SensorData.Humidity, SensorData.Time];
    db.run(sql, parameters, function (err, result) {
      if (err) {
        res.status(400).json({ error: err.message });
        return;
      }
      
      res.json({
        message: "success",
        data: SensorData,
        id: this.lastID,
      });
    });
  });
  
 
  app.get("/Sensors/", (req, res, next) => {
    var sql = "select * from Sensors";
    var parameters = [];
    db.all(sql, parameters, (err, rows) => {
      if (err) {
        res.status(400).json({ error: err.mesasge });
        return;
      }
      res.json({
        message: "success",
        data: rows,
      });
    });
  });
  