import { setTimeout } from 'timers/promises';

export default async (req, res) => {
  if (req.method === 'POST') {
    console.log("POSTed");
    // Get file from request
    const file = req.body;
    // save to txt file
    const fs = require('fs');
    //generate currentdateandstring
    var currentdate = new Date();
    var datetime = currentdate.getDate() + "-"+ (currentdate.getMonth()+1)  + "-" + currentdate.getFullYear() + "-" + currentdate.getHours() + "-" + currentdate.getMinutes() + "-" + currentdate.getSeconds();
    //write to file
    
    fs.writeFile(`./data/acc/${datetime}.txt`, file, function (err) {
      if (err) return console.log(err); 

        const { exec, spawn } = require("child_process");
        var command = `python ".\\checker\\CHECKERDB v2.PY" --platform "Spotify" --file ".//data//acc//${datetime}.txt" --proxies ".//proxies.txt" --email "nk.vashisat@gmail.com"`
        console.log(command)
        //exec(command).stdout.pipe(process.stdout);
        const result_inherited = spawn(command,[], { stdio: 'inherit',shell: true}); // will print as it's processing
      });
    

    


    res.status(200).json({ message: 'Accs added' });
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}