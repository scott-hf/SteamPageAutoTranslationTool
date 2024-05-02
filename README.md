# Steamy Polyglot Pixie
 A Steam store page auto translation tool

This project is intended to be for solo or a small team of indie developers to help with rough english->*** translations. According to some of the data and reports from the Chris Zukowski & the HTMAG community, having translated store pages/names can help increase visibility of your steam products.

NOTE: I have only used and tested this with NEW projects that have yet to be approved by steam. I'm not sure how to apply changes like this to an existing app via the "Steamworks Admin" page once it has already been approved

These translations are SUBPAR AT BEST. It uses a python library from google called Translator. See the python code files for more details.

***USE TRANSLATED VALUES AT YOUR OWN RISK***

Here's how you can use this tool:

**This project does require you to have python installed**

1. The first step is to navigate to the steam partner portal and go to the Steamworks admin page and Store admin page so we can download your base translation files.

![1](https://github.com/scott-hf/Steamy-Polyglot-Pixie/assets/224776/64b94049-292f-4a02-9360-37ee995e1317)

download localization file
![store_name](https://github.com/scott-hf/Steamy-Polyglot-Pixie/assets/224776/0eaf010a-16b6-4d68-b5e3-74222cdb2cfc)

download localization file
![1122](https://github.com/scott-hf/Steamy-Polyglot-Pixie/assets/224776/fd1ad8e9-4432-46c4-a2bc-2710ee9594d8)



(Ensure your page details are filled out in english first before exporting)
![22](https://github.com/scott-hf/Steamy-Polyglot-Pixie/assets/224776/a0cd68d7-5893-4465-acca-73379438b9d6)


2. Next step is to copy these files into the "source" folder from this repo.
3. Then click the translateEverything.bat  

![33](https://github.com/scott-hf/Steamy-Polyglot-Pixie/assets/224776/009993dc-e5cd-40f0-8cfb-62783a1ab69f)
(opsec worryiers, all it does is run the python scripts. feel free to examine the bat script and/or run the python files directly)

now you will find the exported files in the "export" folder. it's time to bring them back into steam

4. upload the contents of exports/appname to the Steamworks Admin page

![44](https://github.com/scott-hf/Steamy-Polyglot-Pixie/assets/224776/8d1e25b3-adde-4f21-869f-5465c58bd3e7)


5. upload the contents of exports/storepage to Store Admin page
![5](https://github.com/scott-hf/Steamy-Polyglot-Pixie/assets/224776/cdbfd2df-3372-42b3-a6a4-6261095c7593)

And that's it. You're done!

If you want to support me, wishlist and spread the word about my upcoming game ProtoZED, a co-op extraction shooter with colony sim elements, inspired by RimWorld and Project Zomboid.
https://store.steampowered.com/app/2360880/ProtoZED/
