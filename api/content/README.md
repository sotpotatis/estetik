# How content is structured

My content is structured as media types (see the main folders: images, sounds, and text.

The final website is going to be divided into segments. A segment could look like this:


```json
{
  "segment_type": "media",
  "media_url": "/api/media/images/image_1.png",
  "text": [{
    "font": "Comic Sans MS",
    "value": "This is a text",
    "size": "2xl"
  }]
}
```
Segments can also be dramatically empty:
```json
{
  "segment_type": "empty"
}
```
And support for rendering new segment types should be added in the `app/`, not here:))

The structure definition for each media type should be put in a `structure.json`
file inside each media type folder.