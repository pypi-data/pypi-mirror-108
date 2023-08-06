# FFenmass

FFenmass is a simple python utility to manipulate in directories and recreate them recursively, inspired by h265ize.

![Demo](example.gif)


### Dependencies
[`ffmpeg`](https://www.ffmpeg.org/)
[`yaspin`](https://github.com/pavdmyt/yaspin)
[`rich`](https://github.com/willmcgugan/rich)


## Installation
```bash
pip3 install ffenmass
```
## Usage



`ffenmass` is transparent above `ffmpeg`, this means all `ffmpeg` syntax can be used with ffenmass as is ,
with the only exception being the input (`-i`) and the output being directories instead of files.
Because `ffenmass` ignores file extensions, you will need to specifify file container using ffmpeg's `-f` argument.




```bash
ffmpeg -i input.mkv -vcodec libx265 out.mkv


python3 ffenmass -i /path/to/media/ -vcodec libx265 -f mkv /output/directory/
```



`ffenmass` will encode all video files detected under the input directory and output them with **the same folder structure and filenames** in the output directory.



**Make sure your input/output directories have a trailing `/`**
```
/path/to/directory   #Is not a valid input

/path/to/directory/  #Is a valid input
```


## Contributing
Open an issue first to discuss what you would like to change.


## Changelogs
 **0.1.1**
 
 - Ignores extensions, will now work with audio,video,subs etc.
 - added pip module



## License
[MIT](https://choosealicense.com/licenses/mit/)
