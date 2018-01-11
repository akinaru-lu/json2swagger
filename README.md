# json2swagger

## Usage
input:
```
$ echo '{ "message": "hello world" }' | python3 main.py
```
output:
```
type:
  object
properties:
  message:
    type:
      string
    example:
      hello world
```
### With prefix and indent
input:
```
$ echo '{ "message": "hello world" }' | python3 main.py -p '# ' -i '**'
```
output:
```
# type:
# **object
# properties:
# **message:
# ****type:
# ******string
# ****example:
# ******hello world
```
## Tips
### Output to stdout
```
$ cat example.json | python3 main.py
```
### Output to file
```
$ cat example.json | python3 main.py > dst.yml
```
### Output to clipborad (example in MacOS)
```
$ cat example.json | python3 main.py | pbcopy
```

### Output
```
type:
  object
properties:
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
