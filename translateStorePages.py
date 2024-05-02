from googletrans import Translator
import json
import os

# Initialize the translator
translator = Translator()

itemidOverride = -1
debugCounterMax = -1
processedCount = 0


jsonKeyNamesToFilterOut = ["language","itemid"]

baseTranslationFile = {}

def sanitize_translated_value(rawValue):
    replacement_string = rawValue
    replacement_string = replacement_string.replace("{steam_app_image} ", "{STEAM_APP_IMAGE}")
    replacement_string = replacement_string.replace("{steam_app_image}", "{STEAM_APP_IMAGE}")
    replacement_string = replacement_string.replace("[img] ", "[img]")
    replacement_string = replacement_string.replace(" [/img]", "[/img]")
    return replacement_string

# Load JSON data from the file
with open("source/storepage_base.json", "r") as file:
    baseTranslationFile = json.load(file)

itemidOverride = baseTranslationFile['itemid']

translationEntriesJsonFileName = "includes/storepage_translations_file"

# Load JSON data from the file
with open(f"{translationEntriesJsonFileName}.json", "r") as file:
    data = json.load(file)

# Translate the "name" field for each entry
for entry in data["entries"]:
    if(debugCounterMax > 0 and processedCount > debugCounterMax):
        break
    
    google_language_id = entry["language"]
    targetLanguage = entry["language"]
    
    if(itemidOverride != -1):
        entry["itemid"] = itemidOverride

    # Use "pt" for Brazilian Portuguese
    if google_language_id == "brazilian":
        google_language_id = "pt"
    
    if google_language_id == "latam":
        google_language_id = "es"
    
    # Map "tchinese" to "zh-TW" for Traditional Chinese
    if google_language_id == "sc_schinese":
        google_language_id = "zh-TW"

    # Map "tchinese" to "zh-TW" for Traditional Chinese
    if google_language_id == "tchinese":
        google_language_id = "zh-TW"
    
    # Map "tchinese" to "zh-TW" for Traditional Chinese
    if google_language_id == "schinese":
        google_language_id = "zh-CN"

    # Map "koreana" to "ko" for Korean
    if google_language_id == "koreana":
        google_language_id = "ko"

    fieldNames = []
    fieldNames = entry.keys()
    # populate fieldNames with a list of field names from entry


    for fieldName in fieldNames:
        if(fieldName in jsonKeyNamesToFilterOut):
            continue
        fieldValue = baseTranslationFile[fieldName]
        if(len(fieldValue) > 1):
            print(f"translating {fieldName} to {targetLanguage}")
            translatedFieldValue = translator.translate(fieldValue, src='en', dest=google_language_id).text
            translatedFieldValue = translatedFieldValue.lower()
            entry[fieldName] = translatedFieldValue

    
    output_directory = f'./exports/export_{entry["itemid"]}/storepage'
    os.makedirs(output_directory, exist_ok=True)

    json_string = json.dumps(entry)
    json_string = json_string.lower()
    sanitized_json_string = sanitize_translated_value(json_string)

    output_file = f'{output_directory}/storepage_{entry["itemid"]}_{entry["language"]}.json'
    with open(output_file, "w") as output_file:
        output_file.write(sanitized_json_string)
    
    processedCount = processedCount+1


mainExportFileName = "temp/storepage_translations_file_translated.json"

# Save the updated data back to the file
with open(mainExportFileName, "w") as file:
    json.dump(data, file, indent=2)

# Print a message to confirm the process is complete
print(f"Translation complete. Updated JSON data saved to {mainExportFileName}.")
