canvas = document.createElement('canvas');
canvas.setAttribute('width', '150px');
canvas.setAttribute('height', '150px');
canvas.setAttribute('id', 'canvas');



responsetxt = document.createElement('textarea');
responsetxt.style.color = '#3DF614';
responsetxt.style.backgroundColor = '#000000';
responsetxt.style.height = '150px';
responsetxt.style.width = '150px';
responsetxt.style.padding = '0px';
responsetxt.style.border = '0';
responsetxt.style.fontSize = '15px';
responsetxt.readOnly = true;


var canvasDiv = document.getElementsByClassName('canvasDiv')[0];
canvasDiv.appendChild(canvas);

var responseDiv = document.getElementById('ans');
responseDiv.appendChild(responsetxt);


if(typeof G_vmlCanvasManager != 'undefined') {
	canvas = G_vmlCanvasManager.initElement(canvas);
}
context = canvas.getContext("2d");

$('#canvas').mousedown(function(e){
  var mouseX = e.pageX - this.offsetLeft;
  var mouseY = e.pageY - this.offsetTop;
		
  paint = true;
  addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
  redraw();
});

$('#canvas').mousemove(function(e){
  if(paint){
    addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
    redraw();
  }
});

$('#canvas').mouseup(function(e){
  paint = false;
});

$('#canvas').mouseleave(function(e){
  paint = false;
});

var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;

function addClick(x, y, dragging)
{
  clickX.push(x);
  clickY.push(y);
  clickDrag.push(dragging);
}

function redraw(){
  context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
  
  context.strokeStyle = "#000";
  context.lineJoin = "round";
  context.lineWidth = 5;
			
  for(var i=0; i < clickX.length; i++) {		
    context.beginPath();
    if(clickDrag[i] && i){
      context.moveTo(clickX[i-1], clickY[i-1]);
     }else{
       context.moveTo(clickX[i]-1, clickY[i]);
     }
     context.lineTo(clickX[i], clickY[i]);
     context.closePath();
     context.stroke();
  }
}

function sendnumber(){
    var imgData = context.getImageData(0, 0, context.canvas.width, context.canvas.height)
    console.log(imgData)
    var data = imgData.data
    
    $.ajax({
        url: '/predict-digit',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        type: 'POST',
        success: function(response){
            // response['digit']
            // response['prob']
        },
        error: function(e){
            console.log(e)
        }
    })
    
    responsetxt.value = 'Your number is: '+ digit + "\\\rand the probabilities are: " + prob;
}


