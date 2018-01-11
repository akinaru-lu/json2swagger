# json2swagger

## Usage
input:
```
$ echo '{ "message": "hello world" }' | python3 main.py
```
output:
```
message:
  type:
    string
  example:
    hello world
```

## Read from file
### Output to stdout
input:
```
$ cat src.json | python3 main.py
```
output:
```
count:
  type:
    integer
  example:
    30
message:
  type:
    string
  example:
    ''
users:
  type:
    array
  items:
    type:
      object
    properties:
      name:
        type:
          string
        example:
          Tom
      id:
        type:
          integer
        example:
          1
      uid:
        type:
          string
        example:
          '000001'
      profile:
        type:
          object
        properties:
          display_name:
            type:
              string
            example:
              Little Tom
          age:
            type:
              integer
            example:
              29
          birthday:
            type:
              string
            example:
              1999-01-03
          location:
            type:
              string
            example:
              ''
          description:
            type:
              string
            example:
              A human\nOr just a cat?\n
last_cursor:
  type:
    integer
  example:
    3673
```
### Output to file
```
cat src.json | python3 main.py > dst.yml
```
### Output to clipborad (example in MacOS)
```
cat src.json | python3 main.py | pbcopy
```
### With prefix and indent
input:
```
cat src.json | python3 main.py -p '# ' -i '**'
```
output:
```
# count:
# **type:
# ****integer
# **example:
# ****30
# message:
# **type:
# ****string
# **example:
# ****''
# users:
# **type:
# ****array
# **items:
# ****type:
# ******object
# ****properties:
# ******name:
# ********type:
# **********string
# ********example:
# **********Tom
# ******id:
# ********type:
# **********integer
# ********example:
# **********1
# ******uid:
# ********type:
# **********string
# ********example:
# **********'000001'
# ******profile:
# ********type:
# **********object
# ********properties:
# **********display_name:
# ************type:
# **************string
# ************example:
# **************Little Tom
# **********age:
# ************type:
# **************integer
# ************example:
# **************29
# **********birthday:
# ************type:
# **************string
# ************example:
# **************1999-01-03
# **********location:
# ************type:
# **************string
# ************example:
# **************''
# **********description:
# ************type:
# **************string
# ************example:
# **************A human\nOr just a cat?\n
# last_cursor:
# **type:
# ****integer
# **example:
# ****3673
```
