import uvage

camera = uvage.Camera(800, 800)

box = uvage.from_color(400, 400, 'red', 50, 50)
box.y = 200
box.speedy = 500
box.move_speed()

print(box.y)
print(box.speedy)
def tick():
	camera.clear("white")
	camera.draw(box)
	camera.display()

uvage.timer_loop(30, tick)