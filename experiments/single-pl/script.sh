../../reservation_generator.py -m "CP7:50,CP9:65,CP10:80,CP11:110,CP12:200" -g "marconi:0" -l 20160 reservations.json > results.txt
../../scheduler.py -g "marconi" -a "plist" -pl "CP12,CP11,CP10,CP9,CP7" -l 20160 reservations.json schedule.json >> results.txt
../../analysis.py schedule.json chart.html >> results.txt
