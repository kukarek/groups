

file1 =  open("C:\\Users\\Dmitry\\Documents\\projects\\bobhell\\image handler\\backgrounds.txt")
a = file1.read()

a = a.split("https://sun9-2.userapi.com/impf/c622929/v622929955/3f914/npNy0kKLmUI.jpg?size=480x854&quality=96&sign=241ba1d9c1b8a90905849f621a8ef8a3&type=album")

file2 = open("C:\\Users\\Dmitry\\Documents\\projects\\bobhell\\image handler\\backgrounds2.txt", "w")
file2.write(a[0])
print()
