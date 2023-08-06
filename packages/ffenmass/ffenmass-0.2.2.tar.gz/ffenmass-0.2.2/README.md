# FFenmass

FFenmass is an FFmpeg python wrapper to manipulate media files in directories enmass and recreate them recursively, inspired by h265ize.
Currently works in **Linux** folder structures only.



### Dependencies
[`ffmpeg`](https://www.ffmpeg.org/)

Yeah you pretty much need Python 3 and ffmpeg installed.Ideally ,moving forward with this project I will try to keep it that way.

<br>

## Installation
```bash
pip3 install ffenmass
```

## Usage



`ffenmass` is transparent above `ffmpeg`, this means most `ffmpeg` syntax can be used with ffenmass as is.


The only differences being the input (`-i`) and the output being directories instead of files.
Also because `ffenmass` ignores file extensions, you will need to specifify container using ffmpeg's `-f` argument.


`ffenmass` will encode all video files detected under the input directory with the provided ffmpeg arguments and output them with **the same folder structure and filenames** in the output directory.

<br>

### Example compared to standard ffmpeg syntax
```bash
ffmpeg -i input.mkv -acodec copy -vcodec libx265 -b:v 2M -minrate 1M -maxrate 3M -preset medium out.mp4


ffenmass -i /path/to/folder/ -acodec copy -vcodec libx265 -b:v 2M -minrate 1M -maxrate 3M -preset medium -f mp4 /output/directory/
```
<br>

Directory Tree visualization of what is going on when you run the command from the example above.
```
path/to/folder/                           /output/directory/
├── givemefolders                         ├── givemefolders      
│   ├── somefolder                        │   ├── somefolder
│   │   └── example_movie.mkv             │   │   └── example_movie.mp4
│   ├── myfavvideo.mkv                    │   ├── myfavvideo.mp4  
│   ├── example_movie.m2ts                │   ├── example_movie.mp4
│   ├── another_example.mkv         →     │   ├── another_example.mp4
│   ├── morefolders                       │   ├── morefolders
│   │   └── a_lot_of_examples.ts          │   │   └── a_lot_of_examples.mp4  
│   └── documentary.mkv                   │   └── documentary.mp4
├── another_example.mkv                   ├── another_example.mp4
├── more-examples.mp4                     ├── more-examples.mp4 
└── examples_and_examples.ts              └── examples_and_examples.mp4

```


<br>

**Make sure your input/output directories have a trailing `/`**
```
/path/to/directory   #Is not a valid input

/path/to/directory/  #Is a valid input
```


## Contributing
Open an issue first to discuss what you would like to change.

Check out the [`changelogs`](CHANGELOGS.md) for notes and todos.

## License
[MIT](https://choosealicense.com/licenses/mit/)
