from setuptools import setup

ld = """
I have noticed that switch/case statements are coming to Python, so I thought it would be amusing to release the 101002938662893028482039th "Missing switch/case package" to this platform.

```python
import switchem

MONKEY = 1
ELEPHANT = 2
GIRAFFE = 3
HORSE = 4
SQUIRREL = 5

for case in switchem(3):
    if case(MONKEY):
        print("It is a monkey")
        break
    
    if case(ELEPHANT, GIRAFFE, HORSE):
        print("It is not a monkey or a squirrel")
    
    if case(SQUIRREL):
        print("It is not a monkey for sure")
```

This has the fall-through behaviour (fall-through will activate as soon as the correct value is checked). It is written in for-loop notation to allow for the use of the `break` keyword. This means that using the `iter` function on these objects will only yield one object.
"""

setup(
    name='switchem',
    packages=["switchem"],
    version='0.1.0',
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    install_requires=["onetrick~=2.1"],
    python_requires="~=3.9",
    long_description=ld,
    long_description_content_type="text/markdown"
)