output "Input a name."
input NAME
output "Hello ", NAME, " nice to meet you!\n\n"

output "Input an integer."
input COUNT as int

if COUNT mod 2 = 0 then
    output COUNT, "is even..."
else
    output COUNT, "is odd..."
end if

output "Enter an integer: "
input INTEGER as int

loop I from 0 to 10
	output I , " x 10 = " , I * 10
end loop
