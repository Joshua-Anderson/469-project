../../reservation_generator.py -m "CP7:50,ADE:53,CP9:65,TST01:72,CP10:80,CP11:110,TST02:200" -g "marconi:0,friis:0,kcc:300,purdue:50,testgs1:150,testgs2:300" -l 20160 reservations.json > results.txt

../../scheduler.py -g "marconi,friis,kcc" -a "token" -pl "CP11,CP10,CP9,CP7,ADE,TST02,TST01" -l 20160 reservations.json schedule1.json >> results.txt
../../scheduler.py -g "purdue" -a "lottery" -l 20160 reservations.json schedule2.json >> results.txt
../../scheduler.py -g "testgs1,testgs2" -a "past24" -pl "TST02,TST01,ADE,CP11,CP10,CP9,CP7" -l 20160 reservations.json schedule3.json >> results.txt

../../analysis.py schedule1.json,schedule2.json,schedule3.json chart.html >> results.txt
