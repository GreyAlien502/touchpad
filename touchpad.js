window.onerror = (msg,url,line) => alert(msg+url+line);
//			Array.from(e.changedTouches).forEach(touch=>JSON.stringify( {
//				x:touch.clientX,
//				y:touch.clientY
//			} ));
let socket = new WebSocket(`ws://${window.location.hostname}:9001`);
let video = document.getElementById("video");

'touchstart touchend touchmove touchcancel'.split(' ').forEach(type=>{
	video.addEventListener(
		type,
		e => {
			e.preventDefault();
			let log = document.getElementById('log');
			//log.innerHTML = (
			//	video.seekable.end(video.seekable.length-1)

				//video.style.transform

			//	type+':\n'+
			//	'changedTouches'.split(' ').map(list=>
			//		Array.from(e[list]).map(touch=>
			//			`${list} : ${touch.identifier}= (${touch.clientX}, ${touch.clientY}) * ${touch.force}`
			//		).join("\n")
			//	).join("\n")
			//) +"\n"+ log.innerHTML;

			//video.play();
			//video.currentTime = video.seekable.end(video.seekable.length-1);
			//()=>video.style.transform = `
			//	scaleX(${document.body.clientWidth / video.clientWidth})
			//	scaleY(${document.body.clientHeight / video.clientHeight})
			//`;

			if(type == 'touchcancel'){
				socket.send({type:type});
			}
			let rect = e.target.getBoundingClientRect();
			Array.from(e.changedTouches).forEach( touch=>
				socket.send(JSON.stringify({
					type:type,
					x:touch.clientX/document.documentElement.clientWidth,
					y:touch.clientY/document.documentElement.clientHeight
				}))
			);
		},
		false
	);

});
//alert("succesS");
