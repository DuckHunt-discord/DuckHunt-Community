import detectlanguage  # pip install detectlanguage
import pydeepl  # pip install pydeepl
import requests
from discord.ext import commands


class DuckSpeak:
    def __init__(self, bot: commands.Bot):
        # Add bot
        self.bot = bot

        # Setup DeepL
        detectlanguage.configuration.api_key = "a481e76cdf524c52fa8ae064baeb397b"
        self.supported = ('DE', 'EN', 'FR', 'ES', 'IT', 'NL', 'PL')  # Languages supported by DeepL

        # Build list of language codes
        languages = requests.get('https://detectlanguage.com/languages.csv')
        languages.raise_for_status()  # Throw an error if unsuccessful
        languages = languages.content.decode('utf-8')[:-1]  # Convert from byte string
        languages = dict([l.split(',') for l in languages.split('\n')])  # Hacky csv parser - who needs true parsing?
        self.languages = languages

    @commands.command()
    async def speak(self, *text):
        text = ' '.join([str(x) for x in text])
        lang = detectlanguage.simple_detect(text).upper()

        if lang not in self.supported:
            await self.bot.say("Sorry, I do not speak {}.".format(self.languages[lang.lower()]))
            return
        else:
            print(f"text={text}, lang={lang}")
            try:
                # Translate English to French and everything else to English
                desired_lang = ('EN', 'FR')[lang == 'EN']
                text = pydeepl.translate(str(text), desired_lang , lang)


            except Exception as e:  # Internal error

                await self.bot.say('Error: {}'.format(e))
                raise

            else:
                pre = ('Translation from DeepL', 'Traduction de DeepL')[lang == 'EN']  # Basic localization
                await self.bot.say('{}```\n{}\n```'.format(pre, text))


def setup(bot: commands.Bot):
    bot.add_cog(DuckSpeak(bot))
