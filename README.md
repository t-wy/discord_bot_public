# Translation:

Notice that the language of translation is based on the locale of the discord User, followed by the guild locale (default to en_US by Discord, but **is ignored** if the guild is not discoverable).

Both full locale (e.g. ja, en-US, zh-TW) and short locale (e.g. ja, en, zh) can be used to specify the translation. "-" should be replaced by "_" when specifying keys or arguments. The priority for locales with subtags is demostrated below:

- `ja`: `ja` → remain unchanged
- `en-US`: `en_US` → `en` → remain unchanged
- `zh-TW`: `zh_TW` → `zh` → remain unchanged

Null (`\0`) is sometimes used as a fallback match that prevents the translator from checking the next available locale. It is used when certain entries do not need to be translated if not specified.

All languages supported by Discord are listed below [Link](https://discord.com/developers/docs/reference#locales):

| LOCALE | LANGUAGE NAME         | NATIVE NAME         | Priority 1 | Priority 2 |
|--------|-----------------------|---------------------|------------|------------|
| id     | Indonesian            | Bahasa Indonesia    | id         |            |
| da     | Danish                | Dansk               | da         |            |
| de     | German                | Deutsch             | de         |            |
| en-GB  | English, UK           | English, UK         | en_GB      | en         |
| en-US  | English, US           | English, US         | en_US      | en         |
| es-ES  | Spanish               | Español             | es_ES      | es         |
| fr     | French                | Français            | fr         |            |
| hr     | Croatian              | Hrvatski            | hr         |            |
| it     | Italian               | Italiano            | it         |            |
| lt     | Lithuanian            | Lietuviškai         | lt         |            |
| hu     | Hungarian             | Magyar              | hu         |            |
| nl     | Dutch                 | Nederlands          | nl         |            |
| no     | Norwegian             | Norsk               | no         |            |
| pl     | Polish                | Polski              | pl         |            |
| pt-BR  | Portuguese, Brazilian | Português do Brasil | pt_BR      | pt         |
| ro     | Romanian, Romania     | Română              | ro         |            |
| fi     | Finnish               | Suomi               | fi         |            |
| sv-SE  | Swedish               | Svenska             | sv_SE      | sv         |
| vi     | Vietnamese            | Tiếng Việt          | vi         |            |
| tr     | Turkish               | Türkçe              | tr         |            |
| cs     | Czech                 | Čeština             | cs         |            |
| el     | Greek                 | Ελληνικά            | el         |            |
| bg     | Bulgarian             | български           | bg         |            |
| ru     | Russian               | Pусский             | ru         |            |
| uk     | Ukrainian             | Українська          | uk         |            |
| hi     | Hindi                 | हिन्दी               | hi         |            |
| th     | Thai                  | ไทย                 | th         |            |
| zh-CN  | Chinese, China        | 中文                | zh_CN      | zh         |
| ja     | Japanese              | 日本語              | ja         |            |
| zh-TW  | Chinese, Taiwan       | 繁體中文            | zh_TW      | zh         |
| ko     | Korean                | 한국어              | ko         |            |

(You may include other translations, but they cannot be reflected on the bot until it is supported by Discord)