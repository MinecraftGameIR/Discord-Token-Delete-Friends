import requests
import threading
import time
import sys
import os

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'

red = colors.RED
green = colors.GREEN
yellow = colors.YELLOW
blue = colors.BLUE
white = colors.WHITE
reset = colors.DEFAULT
bold = colors.BOLD

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    clear()
    title = f"""{green}
╔{'═'*70}╗
║{white}{' '*24}MINECRAFT GAME TOOLS{green}{' '*24} ║
║{white}{' '*27}Version 1.0{green}{' '*28} ║
╚{'═'*70}╝{reset}
    """
    print(title)

def print_banner():
    banner = f"""{green}
╔{'═'*70}╗
║{white}           https://github.com/MinecraftGameIR{green}               ║
║{white}           https://discord.gg/3QYhcRCQAp{green}                    ║
║{white}           https://t.me/MinecraftGame_IR{green}                    ║
║{white}                                                                    {green}║
║{white}                ███╗   ███╗██╗███╗   ██╗███████╗{green}                ║
║{white}                ████╗ ████║██║████╗  ██║██╔════╝{green}                ║
║{white}                ██╔████╔██║██║██╔██╗ ██║█████╗  {green}                ║
║{white}                ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  {green}                ║
║{white}                ██║ ╚═╝ ██║██║██║ ╚████║███████╗{green}                ║
║{white}                ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝{green}                ║
║{white}                                                                    {green}║
║{white}               Discord Friend Management Tool{green}                  ║
╚{'═'*70}╝{reset}
    """


def print_header():
   pass
def current_time_hour():
    return time.strftime('%H:%M:%S')

def get_token():
    print_header()
    print(f"\n{green}[{white}?{green}]{white} Enter Discord Token: {reset}", end="")
    token = input()
    return token.strip()

def validate_token(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None
    except requests.exceptions.Timeout:
        return False, "timeout"
    except requests.exceptions.ConnectionError:
        return False, "connection"
    except:
        return False, "unknown"

def DeleteFriends(friends, token, success_count, error_count):
    for friend in friends:
        try:
            response = requests.delete(
                f'https://discord.com/api/v9/users/@me/relationships/{friend["id"]}',
                headers={
                    'Authorization': token,
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                timeout=10
            )
            
            if response.status_code == 204:
                success_count[0] += 1
                username = friend['user']['username']
                discriminator = friend['user'].get('discriminator', '0000')
                print(f"{green}[{white}{current_time_hour()}{green}]{white} ✓{green} Status: {white}Removed{green} | User: {white}{username}#{discriminator}")
            elif response.status_code == 429:
                try:
                    retry_data = response.json()
                    retry_after = retry_data.get('retry_after', 1)
                except:
                    retry_after = 1
                    
                print(f"{green}[{white}{current_time_hour()}{green}]{yellow} !{green} Rate limited. Waiting {white}{retry_after}{green} seconds...")
                time.sleep(retry_after)
                
                response = requests.delete(
                    f'https://discord.com/api/v9/users/@me/relationships/{friend["id"]}',
                    headers={'Authorization': token, 'Content-Type': 'application/json'},
                    timeout=10
                )
                if response.status_code == 204:
                    success_count[0] += 1
                    username = friend['user']['username']
                    discriminator = friend['user'].get('discriminator', '0000')
                    print(f"{green}[{white}{current_time_hour()}{green}]{white} ✓{green} Status: {white}Removed (retry){green} | User: {white}{username}#{discriminator}")
                else:
                    error_count[0] += 1
                    print(f"{green}[{white}{current_time_hour()}{green}]{red} ✗{green} Failed retry | Status: {white}{response.status_code}")
            elif response.status_code == 404:
                print(f"{green}[{white}{current_time_hour()}{green}]{blue} i{green} Friend not found: {white}{friend['id']}")
            else:
                error_count[0] += 1
                username = friend['user']['username']
                discriminator = friend['user'].get('discriminator', '0000')
                print(f"{green}[{white}{current_time_hour()}{green}]{red} ✗{green} Failed | Status: {white}{response.status_code}{green} | User: {white}{username}#{discriminator}")
                
        except requests.exceptions.Timeout:
            error_count[0] += 1
            print(f"{green}[{white}{current_time_hour()}{green}]{red} ✗{green} Timeout | Friend ID: {white}{friend['id']}")
        except Exception as e:
            error_count[0] += 1
            error_msg = str(e)
            if len(error_msg) > 50:
                error_msg = error_msg[:47] + "..."
            print(f"{green}[{white}{current_time_hour()}{green}]{red} ✗{green} Error: {white}{error_msg}")

def main():
    print_header()
    
    token = get_token()
    
    if not token:
        print(f"\n{green}[{white}!{green}]{white} Token cannot be empty!{reset}")
        input(f"\n{green}[{white}+{green}]{white} Press Enter to exit...{reset}")
        sys.exit(1)
    
    print(f"\n{green}[{white}+{green}]{white} Validating token...{reset}")
    
    is_valid, user_info = validate_token(token)
    
    if not is_valid:
        if user_info == "timeout":
            print(f"\n{green}[{white}!{green}]{white} Connection timeout! Please check your internet.{reset}")
        elif user_info == "connection":
            print(f"\n{green}[{white}!{green}]{white} Connection error! No internet connection.{reset}")
        else:
            print(f"\n{green}[{white}!{green}]{white} Invalid token! Please check your token.{reset}")
        input(f"\n{green}[{white}+{green}]{white} Press Enter to exit...{reset}")
        sys.exit(1)
    
    username = user_info.get('username', 'Unknown')
    discriminator = user_info.get('discriminator', '0000')
    print(f"\n{green}[{white}+{green}]{white} Valid token!{green} User: {white}{username}#{discriminator}")
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"\n{green}[{white}+{green}]{white} Fetching friends list...{reset}")
    
    try:
        response = requests.get(
            "https://discord.com/api/v9/users/@me/relationships",
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            friends_list = response.json()
            if not friends_list:
                print(f"\n{green}[{white}!{green}]{white} No friends found.{reset}")
                input(f"\n{green}[{white}+{green}]{white} Press Enter to exit...{reset}")
                sys.exit(0)
            
            friend_count = len(friends_list)
            print(f"\n{green}[{white}+{green}]{white} Success!{green} Found {white}{friend_count}{green} friends.")
            
            print(f"\n{green}[{white}!{green}]{yellow} WARNING!{green} Are you sure you want to remove ALL {white}{friend_count}{green} friends?")
            print(f"{green}[{white}!{green}]{yellow} WARNING!{green} This action cannot be undone!")
            
            confirm = input(f"\n{green}[{white}?{green}]{white} Type 'YES' to confirm: {reset}")
            
            if confirm.upper() != 'YES':
                print(f"\n{green}[{white}!{green}]{white} Operation cancelled.{reset}")
                input(f"\n{green}[{white}+{green}]{white} Press Enter to exit...{reset}")
                sys.exit(0)
            
            print(f"\n{green}[{white}+{green}]{white} Starting removal process...{reset}")
            print(f"{green}[{white}+{green}]{white} Processing {friend_count} friends in batches...{reset}")
            
            processes = []
            batch_size = 3
            success_count = [0]
            error_count = [0]
            
            start_time = time.time()
            
            for i in range(0, len(friends_list), batch_size):
                batch = friends_list[i:i + batch_size]
                t = threading.Thread(target=DeleteFriends, args=(batch, token, success_count, error_count))
                t.start()
                processes.append(t)
                
                if (i // batch_size) % 5 == 0 and i > 0:
                    time.sleep(0.5)
            
            for process in processes:
                process.join()
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"\n{green}{'═'*70}{reset}")
            print(f"{green}[{white}+{green}]{white} ✓{green} Operation completed in {white}{elapsed_time:.2f}{green} seconds!")
            print(f"{green}[{white}+{green}]{blue} i{green} Total friends: {white}{friend_count}")
            print(f"{green}[{white}+{green}]{white} ✓{green} Successfully removed: {white}{success_count[0]}")
            print(f"{green}[{white}+{green}]{red} ✗{green} Failed to remove: {white}{error_count[0]}")
            print(f"{green}{'═'*70}{reset}")
            
        else:
            print(f"{green}[{white}{current_time_hour()}{green}]{red} ✗{green} Failed to fetch friends: {white}{response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"{green}[{white}{current_time_hour()}{green}]{red} ✗{green} Timeout while fetching friends")
    except Exception as e:
        print(f"{green}[{white}{current_time_hour()}{green}]{red} ✗{green} Error fetching friends: {white}{str(e)}")
    
    input(f"\n{green}[{white}+{green}]{white} Press Enter to exit...{reset}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{green}[{white}!{green}]{white} Operation interrupted by user.{reset}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{green}[{white}!{green}]{white} Unexpected error: {str(e)}{reset}")
        input(f"\n{green}[{white}+{green}]{white} Press Enter to exit...{reset}")
        sys.exit(1)