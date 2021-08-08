<div align="center">
<img src="https://avatars.githubusercontent.com/u/87482214?s=256&v=4" alt="krema"/>
<h1>Krema</h1>
<p>A fast, flexible and lightweight Discord API wrapper for Python.</p>

## Installation

### Unikorn
`unikorn add kremayard krema -no-confirmation`

### Pip
`pip install krema`

## Example Ping-Pong Bot

<div align="left">

```py
from unikorn import krema 
# if you use pip, replace with:
# import krema

client = krema.Client(
    intents=krema.types.Intents().All()
)

@client.event()
async def message_create(message):
    if message.author.bot: return

    if message.content.startswith("!ping"):
        await message.reply(
            content=":ping_pong: Pong!"
        )

client.start("client token", bot=True)
```

</div>

## Todo

<div align="left">

- [x] Add Gateway Support
- [x] Add HTTP Support
- [x] Add Event Handler
- [x] Add Cache System
- [X] Add Models
- [X] Add Functions

</div>

## License

This project is licensed under [MIT](https://opensource.org/licenses/MIT) license.

</div>
