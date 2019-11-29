### Initial Schema of data

```
{
    "name": "Hell-Bound Train",
    "poster": "https://occ-0-3837-2164.1.nflxso.net/art/63d86c81e6f3a8f29cdf24208e36130dc1e36bf63d8e.jpg"
}
```

### For Adding a new key to all documents of collection

```
db.shows.update({}, {$set: {"uploded": false}}, false, true)
```

### After Added new Field

```
{
    "name": "Hell-Bound Train",
    "poster": "https://occ-0-3837-2164.1.nflxso.net/art/63d8e/6c81e6f3a8f29cdf24208e36130dc1e36bf63d8e.jpg",
    "uploaded": false
}
```

### For Deleting a key from all documents of collection

```
db.shows.updateMany({}, {$unset:{"uploded":1}})
```

### For Selecting only imp fields

```
cursor = db.shows.find({"uploded": false}, {"posters": 1})
```
This operation corresponds to the following SQL statement:

```
SELECT _id, item, status from inventory WHERE status = "A"
```

### Counting Upload Complete

```
db.shows.find({"uploded" : true}).count() 
```