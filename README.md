# WhatsApp Bot

**Objetives:**

-   Show an image with the QR code to log in: ✅
-   Handle incoming messages: ✅
-   Create a command handler: ❌
    -   Handle commands with arguments: ❌
    -   Handle commands with images: ❌
    -   Handle commands by role: ❌
-   Save users & executed commands in the DB: ❌
-   Ignore messages from banned users: ❌

**Commands:**

-   /menu ❌
    -   Returns a list of all the available commands.
-   /say _\<message>_ ❌
    -   Says the received message.
-   /send _\<phone number>_**;**_\<message>_ ❌
    -   Sends a message to a specified phone number (clarifying that it is your message).

**Admin commands:**

-   /ban _\<phone number>_**;**_\<reason>_ ❌
    -   Bans the given phone number due to a reason.
-   /role _\<phone number>_**;**_\<role>_ ❌
    -   Sets a role for a given phone number.
-   /pfp _(with an image)_ ❌
    -   Sets the given image as profile picture.
-   /status _\<message>_ ❌
    -   Sets the given message as profile status.
