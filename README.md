# WhatsApp Bot

**Objetives:**

-   Show an image with the QR code to log in: ✅
-   Handle incoming messages: ✅
-   Create a command handler with:
    -   Image handling: ✅
    -   Argument handling: ✅
    -   Role handling: ❌
-   Save in the DB:
    -   Users: ✅
    -   Banned Users: ✅
    -   Roles: ✅
    -   User Roles: ✅
    -   Commands: ✅
    -   Executed Commands: ✅
-   Create i18n for these languages:
    -   Spanish: ❌
    -   Portuguese: ❌
    -   Italian: ❌
    -   French: ❌
    -   German: ❌

**Commands:**

-   /menu ✅
    -   Returns a list of all the available commands.
-   /whoami ✅
    -   Tells you who you are.
-   /sticker _(with an image)_ ✅
    -   Creates a sticker with an image that you provide.
-   /say _\<message>_ ✅
    -   Replies with the message you sent..
-   /send _\<phone number>_**;**_\<message>_ ✅
    -   Sends a message to a specified phone number, clarifying that it is your message.

**Commands by role:**

-   /resources ❌
    -   Returns details about CPU and RAM usage.
    -   Requires **MODERATOR** role or higher.
-   /history _\<phone number>_**;**_\<limit?>_ ❌
    -   Returns the command history of an user, with an optional limit.
    -   Requires **MODERATOR** role or higher.
-   /executions _\<command name>_ ❌
    -   Returns the number of times a command has been executed.
    -   Requires **MODERATOR** role or higher.
-   /pfp _(with an image)_ ❌
    -   Sets the given image as profile picture.
    -   Requires **ADMIN** role.
-   /status _\<message>_ ❌
    -   Sets the given message as profile status.
    -   Requires **ADMIN** role.
-   /ban _\<phone number>_**;**_\<reason>_ ❌
    -   Bans the given phone number due to a reason.
    -   Requires **ADMIN** role.
-   /role _\<phone number>_**;**_\<role>_ ❌
    -   Sets a role for a given phone number.
    -   Requires **ADMIN** role.
