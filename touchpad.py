import sys, os, traceback, urllib.parse, http.server, mimetypes, http.client, shelve, subprocess, multiprocessing, json, types, io, tkinter
import websocket_server, pyautogui, mss, PIL
import je3.server, je3.errors, je3.tags, je3.storage

pyautogui.PAUSE=0
t = je3.tags.tagSource

bounds = multiprocessing.Manager().list()


multiprocessing.Process(target=lambda window=...:(
	window := tkinter.Tk(),
	window.wait_visibility(window),
	window.wm_attributes('-alpha', 0.3),
	window.bind('<Configure>',lambda event:
		bounds.__setitem__(slice(None,None),[
			max(0,min(window.winfo_screenwidth(),event.x)),
			max(0,min(window.winfo_screenheight(),event.y)),
			max(0,min(window.winfo_screenwidth(),event.x+event.width)),
			max(0,min(window.winfo_screenheight(),event.y+event.height)),
		])
		if event.widget is window else ...
	),
	window.mainloop(),
)).start()






def getJS():
	print('ok')
	return [subprocess.check_output('npx babel --presets es2015 touchpad.js',shell=True).decode(),print("oKK")][0]

def handle_http(request):
	path = urllib.parse.urlparse(request.path).path
	try:
		if path == '/':
			return je3.server.response(t.html(
				t.head(
					t.meta(name='viewport', content='width=device-width'),
					t.style("""
						body, html {
							width: 100%;
							height: 100%;
							margin: 0;
							padding: 0;
							overflow: hidden;
							user-select: none;
							-webkit-touch-callout:none;
							-webkit-user-select:none;
							-khtml-user-select:none;
							-moz-user-select:none;
							-ms-user-select:none;
							user-select:none;
							color:#0ff;
							background-color:#000;
						}
						#video{
							max-width: 100%;
							max-height: 100%;
							width: auto;
							height: auto;
							margin: auto auto;
						}

					"""),
				),
				t.body(
					t.pre(id='log'),
					t.img(
						id="video",
						src='/img.jpg?size=[1,1]',
						onLoad="this.src='/img.jpg?size='+JSON.stringify([document.documentElement.clientWidth,document.documentElement.clientHeight])+'&t='+Math.random();",
					),
					#t.video(
					#	t.source(src="http://192.168.1.3:3000/index.m3u8",type="application/x-mpegURL"),
					#	style="width:100vw; height:100vh",
					#	autoplay="",
					#	muted="",
					#	playsinline="",
					#	id="video",
					#),
					t.script(getJS()),
				)
			).encode())
		elif path == '/img.jpg':
			with mss.mss() as sct:
				screenshot = sct.grab( tuple(bounds) )
				with io.BytesIO() as output:
					PIL.Image.frombytes(
						"RGB", screenshot.size, screenshot.bgra, "raw", "BGRX"
					).resize(
						json.loads(je3.server.query(request)['size'])
					).save(
						output, format="JPEG"
					)
					return je3.server.response(
						output.getvalue(),
						code=200,
						headers={
							"Content-type":"image/jpeg",
							"Connection":"keep-alive",
							"Keep-Alive": "timeout=10",
						}
					)
		raise je3.errors.HTTPError(404)
	except Exception as e:
		if isinstance(e, je3.errors.HTTPError):
			return e.response()
		the_traceback  = ''.join(traceback.TracebackException.from_exception(e).format())
		print(the_traceback)
		return je3.server.response(
			code=500,
			body=t.pre(the_traceback).encode()
		)

multiprocessing.Process(target=lambda:
	http.server.ThreadingHTTPServer(
		('0.0.0.0',int(sys.argv[1])),
		je3.server.handler(handle_http,connection_timeout=1)
	).serve_forever()
).start()









def handle_touch(client,server,message):
	event = types.SimpleNamespace(**json.loads(message))
	width,height = pyautogui.size()
	if event.type != 'touchcancel':
		x,y = bounds[:2]
		width,height = bounds[2]-x, bounds[3]-y
		pyautogui.moveTo(bounds[0]+event.x*width,bounds[1]+event.y*height)
	dict(
		touchstart=pyautogui.mouseDown,
		touchend=pyautogui.mouseUp,
		touchcancel=pyautogui.mouseUp,
		touchmove=lambda:None,
	)[event.type]()

server = websocket_server.WebsocketServer(port=9001, host='0.0.0.0')
server.set_fn_message_received(handle_touch)
server.run_forever()
