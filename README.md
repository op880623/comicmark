# A WEBSITE RECORDS THE PROGRESS OF MY COMIC READING

The target site is [this](http://www.cartoonmad.com/).

## Object
### comic
```
from comic.models import Comic
comic = Comic.new(comicId=4444)
comic.update()
comic.update(13)
```
`new` creates object if object doesn't exist.
And it automatically determines name and url of the comic.

`update` creates Episode objects of the comic which are not be read.
If no progress is given, it tries to use `comic.progress`, or get all episodes.

## command
1. updateall
```
python manage.py updateall
```
Update all comic without giving progress

2. addcomic
```
python manage.py addcomic
```
It takes comicId and progress(optional) as parameters, and functions as `new` then `update`.

3. progress_to_json
```
python manage.py progress_to_json
```
return json string as output like below.
```
[{"comicId": 4444, "index": 13}, {"comicId": 5555, "index": 14}]
```
