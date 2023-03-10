# WhatsApp Bot

This WhatsApp Bot was made with **Python** using the _Selenium_ library and **PostgreSQL** for the database.

**Disclaimer:** This bot only works in Windows and you need to have Brave Browser installed in your system.

## Requirements:

-   All the dependency requirements are included in the `requirements.txt` file.
-   Install the database from the `db.sql` file.
-   Add your database credentials in a `.env` file with the variables:
    -   `DB_HOST`: The database host.
    -   `DB_NAME`: The database name.
    -   `DB_USERNAME`: The database username.
    -   `DB_PASSWORD`: The database password.
-   The WhatsApp phone application must have:
    -   A pinned chat to focus on.
    -   No access to your contacts.

## Creating the executable:

Execute this command in your terminal:
`pyinstaller ./src/main.py --name WhatsAppBot --onefile --clean --distpath ./build --specpath ./build --version-file ../version.rc --icon ../icon.ico --key SOME_KEY`

You can replace SOME_KEY with the one you prefer.

## Objetives:

-   Show an image with the QR code to log in: ✅
-   Handle incoming messages: ✅
-   Create a command handler with:
    -   Image handling: ✅
    -   Argument handling: ✅
    -   Role handling: ✅
-   Save in the DB:
    -   Users: ✅
    -   Banned Users: ✅
    -   Roles: ✅
    -   User Roles: ✅
    -   Commands: ✅
    -   Executed Commands: ✅
-   Available languages:
    -   English: ✅
    -   French: ✅
    -   German: ✅
    -   Italian: ✅
    -   Portuguese: ✅
    -   Spanish: ✅

#### Global commands:

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
-   /random _\<number | image | quote>_ ✅
    -   Replies with a random number/image/quote.

#### Staff commands:

-   /resources ✅
    -   Returns details about CPU and RAM usage.
    -   Requires **MODERATOR** role or higher.
-   /history _\<phone number>_**;**_\<limit?>_ ✅
    -   Returns the command history of an user, with an optional limit.
    -   Requires **MODERATOR** role or higher.
-   /executions _\<command name>_ ✅
    -   Returns the number of times a command has been executed.
    -   Requires **MODERATOR** role or higher.
-   /user _\<phone number>_ ✅
    -   Returns information about an user.
    -   Requires **MODERATOR** role or higher.
-   /pfp _(with an image)_ ❌
    -   Sets the given image as profile picture.
    -   Requires **ADMIN** role or higher.
-   /status _\<message>_ ❌
    -   Sets the given message as profile status.
    -   Requires **ADMIN** role or higher.
-   /ban _\<phone number>_**;**_\<reason>_ ✅
    -   Bans the given phone number due to a reason.
    -   Requires **ADMIN** role or higher.
-   /unban _\<phone number>_ ✅
    -   Unbans the given phone number.
    -   Requires **ADMIN** role or higher.
-   /role _\<phone number>_**;**_\<role name>_ ✅
    -   Sets a role for a given phone number.
    -   Requires **OWNER** role.

## Media

https://user-images.githubusercontent.com/91042041/213880294-c034e310-8edc-4ba0-9e81-c8840767e295.mp4

![Chat Image](https://user-images.githubusercontent.com/91042041/213880331-4f52bf85-3ff4-4f3d-b70c-3ab25d6c1dc1.png)
