// main menu sliding code

document.getElementById('main').addEventListener('mousemove',function(e){
	if (document.body.offsetWidth<1024){
	if (e.offsetX <= 40) {
		document.getElementById('nav').style.left = "0";
		document.getElementById('main').style.marginLeft = "40px";
	}
	else{
		document.getElementById('main').style.marginLeft = "0";
		document.getElementById('nav').style.left = "-40px";
		document.getElementById('menu').style.display='none';
		document.getElementById('nav').firstElementChild.style.color = '#fff';
		document.getElementById('wallet').style.left = '-400px';

	}
  }
})

function menuDisp() {
	let x = document.getElementById('menu');
	if (x.style.display=='none') {
		x.style.display='block';
		document.getElementById('nav').firstElementChild.style.color = '#f48020';
		document.getElementById('wallet').style.left = '-400px';
		
	}
	else{
		x.style.display='none'
		document.getElementById('nav').firstElementChild.style.color = '#fff';
	}
}

if (document.body.offsetWidth>1024) {
		document.getElementsByClassName('sdasdasd')[0].className += " p-0 pr-1";
		document.getElementsByClassName('sdasdasd')[1].className += " p-0 pl-1";
	}