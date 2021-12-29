# pix2txt

Optical Character Recognition (OCR) [telegram](https://telegram.org/) bot built using python that extracts texts found inside pictures.

## usage

1. ```/start``` the bot [@pix2txt_bot](https://t.me/pix2txt_bot)
2. Just send a picture to the bot as you normally would without a caption -- captions & any other texts outside of the picture are unnecessary.
3. It also supports forwarded picture messages.
4. If you want further help, just send ```/help```

## libraries employed

- [ocrspace](https://github.com/ErikBoesen/ocrspace)
- [telethon](https://github.com/LonamiWebs/Telethon)

## how to run

1. create a virtual environment, source it and install -- upgrade if you wish -- all dependencies found inside requirements.txt by doing ```pip install -U -r requirements.txt```

2. get your own API_ID & API_HASH from <https://my.telegram.org/auth>

3. create a telegram bot using [@botfather](https://t.me/botfather)

4. get bot's token from [@botfather](https://t.me/botfather)

5. create a ```.env``` file in the root directory  and place the above details inside it as such:

        TOKEN = xxxxxxx
        API_ID = xxxxxx
        API_HASH = xxxxxxxx

6. run it just as any python application by ```python src/botter.py```

## Caveats

It only recognizes LATIN characters.
