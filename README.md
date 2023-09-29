# FarCloud
This is Python program to manage your DNS on cloudflare

# Requirements

Python libraries to install before starting:
* requests
* os (you may already has it)
* re (you may already has it)
* dotenv


>[!IMPORTANT]
>
>You must create .env file with structure of .env.example and write your data. 



# Usage

You can use it very easly. 
use

```
python3 main.py
```

Now you are able to use this script and see the menu to manage your dns. 

# Options

You have many option for FarCloud:
| Option | Description |
|---|---|
| Scan all Records | Scan all your records of your dns |
| Change record | change the ip of all record with type A, this i useful for little dns to change all subdomain |
| Add record | add record putting the type as 'A' or 'MX' and writing the ip address |
| Remove record | remove record using name, if you write *hello* and it will automatically concatenate the name and site using in .env file as *hello.site.com*


