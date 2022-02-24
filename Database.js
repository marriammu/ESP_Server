var sqlite3 = require("sqlite3").verbose();

const Databases = "db.sqlite";

let db = new sqlite3.Database(Databases, (err) => {
  if (err) 
  {
    console.error(err.message);
  } 
  else {
    console.log("Connected to the Database database in sqlite.");
    db.run(
      `CREATE TABLE Sensors (ID INTEGER PRIMARY KEY AUTOINCREMENT,Temperature text, Humedity text, Time text)`,
            console.log('Table Created'),
            (err) => {
                if (err) {
                  // Table already created
                } else {
                  // Table just created, creating some rows
                    
                }
              }
              );
  }
});

module.exports = db;
