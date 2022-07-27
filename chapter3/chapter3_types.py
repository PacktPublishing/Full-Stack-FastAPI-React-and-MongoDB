def annotated_function(name: str, age: int)->str:
	return f"Your name is {name.upper()} and you are {age} years old!"

print(annotated_function(name="marko", age=99))