		var _year;
		var _month;
		var _day;
		var display_date;
		var json_Data;
		var previous_day;
        var today;
        var run =0;
        
		$(document).ready( function() {
		
			setDisplayDate();
            today = true;
		
		});
		
		function setDisplayDate() {
			$(".table").empty();
			$(".table").append("<tr class ='header'><th>Request ID# </th></tr>");
			$(".norequests").empty();
			$(".number").empty();
			$(".amount").empty();
            
            if (run > 0) {
                today = false;
            }
			
            if(today === false) {
			display_date = document.getElementById("filter_date").value;

			 _year = parseInt(display_date.slice(0,4));
			 _month = parseInt(display_date.slice(5,7));
			 _day = parseInt(display_date.slice(8,11)) -1;
			if(_month.length == 2) {
			 previous_day = _year+ "-" + _month + "-" + _day;
			 } else {
				previous_day = _year + "-0" + _month + "-" + _day;
			 }
            } else {
                display_date = new Date();
                _year = display_date.getFullYear();
                _month = display_date.getMonth() + 1;
                _day = display_date.getDate() -1;
            
            if(_month.length == 2) {
			 previous_day = _year+ "-" + _month + "-" + _day;
             display_date = _year + "-" + _month + "-" + (_day+1);
             console.log(display_date);
			 } else {
				previous_day = _year + "-0" + _month + "-" + _day ;
                display_date = _year + "-0" + _month + "-" + (_day + 1);
                console.log(display_date);
			 }
            }
			

			 var config;
			$.get("https://townofchapelhill.github.io/scf-reconciliation/config_bulky_items.txt", function(data) {
				config = data.split("\n");
				for(var s in config) config[s] = config[s].trim();
            });
			 
			 
			 $.getJSON("https://townofchapelhill.github.io/scf-reconciliation/seeclickfix_bulky_items.json",
            function processData(jsonData) {
			   var totalRequests = 0;
                var sumTotal = 0;
                
				var firstLoop = true;
				var questions = new Map();
				var are_requests = false;
				
				$.each(jsonData.issues, function (object, objectData) {
					
					if(objectData.created_at.slice(0,10) === display_date  && parseInt(objectData.created_at.slice(11,13)) < 17
				   || objectData.created_at.slice(0,10) === previous_day && parseInt(objectData.created_at.slice(11,13)) >= 17 ) {
						
					if(firstLoop){
						for (var i in config) for(var q in objectData.questions) if(config[i] === objectData.questions[q].question.trim()){ 
							questions.set(config[i], q);
							$(".header").append("<th>" + config[i] + "</th>");
							break;
						}
						firstLoop = false;
					}
					
					var output = "<tr><td>" + objectData.id + "</td>";
					for(var i of questions.values()) output += "<td>" + getAnswer(objectData.questions, i) + "</td>";
					output += "</tr>";
					$("table").append(output);
					are_requests = true;
					totalRequests++;
					if(questions.has("Amount paid") && objectData.questions != null && !isNaN(getAnswer(objectData.questions, questions.get("Amount paid")))) sumTotal += parseInt(getAnswer(objectData.questions, questions.get("Amount paid")));

					 
				}
                    
                });
				
				if(are_requests === false) {
                    if(today === false){
					$(".norequests").append("There are no requests in this time range.");
                    } else {
                    $(".norequests").append("There are no requests from today.");
                    }
				}else{
					$(".number").append("The Total Number of Requests is " + totalRequests);
					$(".amount").append("The Amount Paid Sum is " + sumTotal + " dollars");
				}
				
			});
            run++;
		}
			
		//Returns the answer to a given question in a list of questions.
		function getAnswer(questions, num){
			if(questions === null) return "No Answer Given (null)";
			if(questions[num] === null) return "No Answer Given (null)";
			return questions[num].answer
		}
		
        function downloadCSV(csv,filename) {
            var csvSCF;
            var downloadLink;
            
            csvSCF = new Blob([csv], {type: 'text/csv' });
            
            downloadLink = document.createElement("a");
            
            
            downloadLink.download = filename;
             //creating a link to the file
             //pasing in the new CSV object
             downloadLink.href = window.URL.createObjectURL(csvSCF);
             downloadLink.style.display = 'none';
             document.body.appendChild(downloadLink);
             downloadLink.click();
               
    }
        function exportTableToCSV(filename) {
        
			var csv = [];
			var rows = document.querySelectorAll("table tr");
        
			for (var i = 0; i < rows.length; i++) {
				//assigning each row of the csv fileto be the td elements from the table
				var row = [], cols = rows[i].querySelectorAll("td, th");
        
				for (var j = 0; j < cols.length; j++) row.push(cols[j].innerText);
				
				for(var k in row) row[k] = "\"" + row[k] + "\""
				
				csv.push(row.join(","));
			}
			
			// Download CSV file
			downloadCSV(csv.join("\n"), filename);
      
		}