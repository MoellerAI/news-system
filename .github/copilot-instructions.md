## code style

You always add typehints for but input variables and return values. But also for local variables inside methods or attributes. 

You always add docstring to all methods and classes. You follow the Google docstring format.

## Comptetences

You are an expert in Python and you are able to write code that is efficient, readable, and maintainable. You are also familiar with the latest Python features and libraries. You have a strong understanding of design patterns and best practices in software development and always strive at choosing the best solution for the problem at hand.

## Package management

You use Astral's `uv` package management system to manage dependencies. You always specify the version of the package you are using and you use the `uv add` command to add new packages.

## Testing

You always write tests for your code. You use the `unittest` framework and you follow the Arrange-Act-Assert (AAA) pattern. You also use `pytest` to run your tests and you always run your tests before committing your code.

## repo structure

You find StrEnum's and pydantic BaseModel's in the `app/src/schemas` folder. Most are defined in base.py file in the folder. 

The system are built using a lot of "roles" defined by abstract classes in the `app/src/roles` folder. The roles are used to define the behavior of the system and are implemented by concrete classes in the `app/src/news_rooms` folder.