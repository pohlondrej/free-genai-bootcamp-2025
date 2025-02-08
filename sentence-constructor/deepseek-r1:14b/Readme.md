## Model
[deepseek-r1:14b](https://ollama.com/library/deepseek-r1)

## Basic exploration (getting to know the model)
### Do you know Japanese?
Yes, I can understand and communicate in Japanese to some extent. If you have any questions or need assistance in Japanese, feel free to ask! 😊
### How many parameters you have?
As an AI language model, **I don’t have direct access** to specific details about my architecture or parameter count.
### Can you create tables?
- Yes, I can create tables using text! Here's an example of how I can format a table: \*provides a table*\
    - NOTE: At this point, Gemini already put Japanese into the table. The example table from DeepSeek is very barebones.
### Can you make English - Japanese vocabulary flashcards in .csv format, so that I can build an Anki deck?
- provides 22 random words and sentences, example: `Hello,こんにちは (Konnichiwa)`
- gives very brief instructions on how to import cards to Anki...not sure if the instructions are 100%correct
    - honestly, for a 14B offline model it's impressive it even knows what Anki is
### Do you understand Markdown and XML? Can I give you advanced prompts using Markdown and XML?
Yes, I understand Markdown to some extent and can interpret basic Markdown syntax. However, I do not natively understand or process XML.
### Is there a way to give you good and bad examples to help you understand the query?
^ So, the user is looking for a way to improve my comprehension of their requests by giving examples. They might be trying to figure out how to make their interactions with me more effective, especially since I'm an AI that relies on clear instructions.
- then it proceeds to explain I can give it examples in Markdown; worth a shot?


## Attempts
### Attempt \#1
- Using the same prompt as the last Gemini prompt, since Gemini absolutely crushed it and didn't need much handholding.
- "Wait, I'm getting tangled up here. Let me take a step back." - Ooof. It's struggling!
- Puts Kanji inside Hiragana column. Not good.
- Provides examples in the sentence structure, even though it was not told to do so.
- Thinks for 6 minutes!! (maybe I need to reduce the reasoning effort parameter in Ollama)
- Worst of all, doesn't understand the concept of role playing. Seems like I need to use different approach.

### Attempt \#2
OK, this was tough. I might have spent 2 hours trying to produce a meaningful answer. Choosing a small locally hosted model was not a good idea.
- Let's start with the positives:
    - I managed to get a table with correct words, and a correct sentence structure. That's a win.
    - After giving answer in Japanese, I managed to receive an answer where the model corrected me, although not perfectly.
After that, everything went downhill:
- Hardest part was to make the model to *not* put kanji in the hiragana column.
- The model overthinks a lot. Generating an answer on my computer takes 5-10 minutes, because the model keeps getting lost in thoughs, even after reducing the reasoning effort parameter.
    - Is the context too small?
- It seems to be incapable of understanding `[After waking up]`, and refuses to make a structure out of it.
- Afer answering correctly, it recommends adding 私は, even though it can be omitted.
- When I tried second English sentence, the model completely forgot what it's supposed to do, and straight up translated the English sentence to Japanese. That's a fail.