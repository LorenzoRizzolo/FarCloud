import requests
import os
from dotenv import load_dotenv
import re

load_dotenv()

api_token = os.getenv('API_TOKEN')
zone_id = os.getenv('ZONE_ID')
site = os.getenv('SITE')

regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


def add_dns_record(api_token, zone_id, name, ip_address):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Define the payload for creating a new DNS record of type A
    payload = {
        "type": "A",
        "name": name,  # Specify the name (subdomain) for the record
        "content": ip_address,  # Specify the IP address
        "ttl": 1,  # Time-to-live (TTL) in seconds
        "proxied": True  # Set to True if you want to proxy the traffic through Cloudflare
    }

    # Send a POST request to create the DNS record
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Added DNS record for {name} with IP {ip_address}")
    else:
        print(f"Failed to add DNS record. Status code: {response.status_code}")
        
def get_dns_records():
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["result"]
    else:
        print(f"Request failed with status code {response.status_code}")
        return []

def update_dns_record(record_id, new_ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": new_ip
    }

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        return "Record updated"
    else:
        return f"Request failed with status code {response.status_code}"

def add_dns_record(typ, name, ip_address):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Define the payload for creating a new DNS record of type A
    payload = {
        "type": typ,
        "name": name,  # Specify the name (subdomain) for the record
        "content": ip_address,  # Specify the IP address
        "ttl": 1,  # Time-to-live (TTL) in seconds
        "proxied": True  # Set to True if you want to proxy the traffic through Cloudflare
    }

    # Send a POST request to create the DNS record
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return f"{name} added to {site}"
    else:
        return f"Failed to add DNS record. Status code: {response.status_code}"

def delete_dns_record_by_name(name):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        dns_records = data["result"]
        for record in dns_records:
            if record["name"] == name:
                # Construct the URL for deleting the DNS record
                delete_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}"
                
                # Send a DELETE request to delete the DNS record
                response = requests.delete(delete_url, headers=headers)
                
                if response.status_code == 200:
                    return f"Deleted DNS record with name {name}"
                else:
                    return f"Failed to delete DNS record with name {name}. Status code: {response.status_code}"
    
    else:
        return f"Failed to fetch DNS records. Status code: {response.status_code}"

def title(t):
    print("------------- "+t+" -------------\n")

def valid_ip(ip):
    if(re.search(regex, ip)):
        return 1
    else:
        return 0

def scan_dns():
    dns_records = get_dns_records()
    print("")
    for record in dns_records:
        print(f"Name: {record['name']}, Type: {record['type']}, Value: {record['content']}")
    print("")
    
def exist_record(name):
    check_dns = 0
    dns_records = get_dns_records()
    for record in dns_records:
        if record['name']==name+"."+site:
            check_dns=1
    return check_dns
    
def get_ip_record(rec):
    check_dns = 0
    dns_records = get_dns_records()
    for record in dns_records:
        if record['name']==rec:
            return record['content']
    return check_dns
    
def change_ip():
    new_ip = input("Enter new ip for A records: ")
    print("")
    if valid_ip(new_ip)==1:
        dns_records = get_dns_records()
        for record in dns_records:
            sub = record['name'].split(".")[0]
            if sub!="mx" and record['type']=="A":
                end = update_dns_record(record['id'], new_ip)
                print(record['name']+": "+end)
        print("")
    else:
        print("Invalid IP addres "+str(new_ip))
    
def add_record():
    typ = input("Enter the type of new record: ")
    name = input(f"Enter name of new {typ} record: ")
    if exist_record(name)==0:
        ip = get_ip_record(site)
        if valid_ip(ip)==1:
            end = add_dns_record(typ.upper(), name, ip)
            print(end)
    else:
        print(name+" already esists")
        
def del_record():
    name = input("Enter name of record to delete: ")
    if exist_record(name)==1:
        end = delete_dns_record_by_name(f"{name}.{site}")
        print(end)
    else:
        print(f"{name}.{site} doesn't esist")

def switch_opt(choose):
    if choose=="0":
        title("RECORDS")
        print("Wait...")
        scan_dns()
        exit = input("Press something to continue...\n")
        return 1
    elif choose=="1":
        title("CHANGE IP")
        change_ip()
        return 1
    elif choose=="2":
        title("Add record")
        add_record()
        print("")
        return 1
    elif choose=="3":
        title("Delete record")
        del_record()
        print("")
        return 1
    elif choose=="x":
        return 0
    else:
        print(f"\nOpzione {choose} non valida\n")
    return 1
    
    
# ---------------------START------------------------
title("WELCOME TO FARCLOUD")
title("START")
print("Checking token and zoneid...")
if api_token == "":
    print("API TOKEN isn't set.")
    print("You must set it into .env file in this directory as .env.example")
    exit()
if zone_id == "":
    print("ZONE ID isn't set.\n")
    print("You must set it into .env file in this directory as .env.example")
    exit()
if site == "":
    print("SITE isn't set.\n")
    print("You must set it into .env file in this directory as .env.example")
    exit()
    
print("Token, site and Zone id ok.\n")

check=1
while check==1:
    title("MENU")

    opt = [ "Scan your records" , "Change ip of all A records" , "Add record" , "Remove record A" ]

    for index, op in enumerate(opt):
        print("["+str(index)+"]", op)
    print("[x] Exit")

    op = input("Choose option (enter number): ")
    check = switch_opt(op)
    
print("Exit...")
    



