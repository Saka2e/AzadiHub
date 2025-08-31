import os
import base64
import requests
import binascii
import pybase64
from django.conf import settings
from crawler.models import Config

# Define a fixed timeout for HTTP requests
TIMEOUT = 15  # seconds

# Define the fixed text for the initial configuration
fixed_text = """#profile-title: base64:8J+GkyBHaXRodWIgfCBCYXJyeS1mYXIg8J+ltw==
#profile-update-interval: 1
#subscription-userinfo: upload=29; download=12; total=10737418240000000; expire=2546249531
#support-url: https://github.com/barry-far/V2ray-config
#profile-web-page-url: https://github.com/barry-far/V2ray-config
"""

# Base64 decoding function
def decode_base64(encoded):
    decoded = ""
    for encoding in ["utf-8", "iso-8859-1"]:
        try:
            decoded = pybase64.b64decode(encoded + b"=" * (-len(encoded) % 4)).decode(encoding)
            break
        except (UnicodeDecodeError, binascii.Error):
            pass
    return decoded

# Function to decode base64-encoded links with a timeout
def decode_links(links):
    decoded_data = []
    for link in links:
        try:
            response = requests.get(link, timeout=TIMEOUT)
            encoded_bytes = response.content
            decoded_text = decode_base64(encoded_bytes)
            decoded_data.append(decoded_text)
        except requests.RequestException:
            pass  # If the request fails or times out, skip it
    return decoded_data

# Function to decode directory links with a timeout
def decode_dir_links(dir_links):
    decoded_dir_links = []
    for link in dir_links:
        try:
            response = requests.get(link, timeout=TIMEOUT)
            decoded_text = response.text
            decoded_dir_links.append(decoded_text)
        except requests.RequestException:
            pass  # If the request fails or times out, skip it
    return decoded_dir_links

# Filter function to select lines based on specified protocols and remove duplicates
def filter_for_protocols(data, protocols):
    filtered_data = []
    seen_configs = set()
    
    # Process each decoded content
    for content in data:
        if content and content.strip():  # Skip empty content乞ادم content
            lines = content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('#') or not line:
                    # Always keep comment/metadata/empty lines
                    filtered_data.append(line)
                elif any(protocol in line for protocol in protocols):
                    if line not in seen_configs:
                        filtered_data.append(line)
                        seen_configs.add(line)
    return filtered_data

# Create necessary directories if they don't exist
def ensure_directories_exist():
    output_folder = os.path.join(settings.BASE_DIR, 'static')
    base64_folder = os.path.join(output_folder, 'Base64')
    protocol_folder = os.path.join(output_folder, 'Splitted-By-Protocol')

    for folder in [output_folder, base64_folder, protocol_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    return output_folder, base64_folder, protocol_folder

# Main function to process links, filter configs, and save to database and files
def main():
    output_folder, base64_folder, protocol_folder = ensure_directories_exist()

    # Clean existing output files
    print("Cleaning existing files...")
    output_filename = os.path.join(output_folder, "All_Configs_Sub.txt")
    main_base64_filename = os.path.join(output_folder, "All_Configs_base64_Sub.txt")
    
    for file_path in [output_filename, main_base64_filename]:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed: {file_path}")

    for i in range(1, 21):
        filename = os.path.join(output_folder, f"Sub{i}.txt")
        filename_base64 = os.path.join(base64_folder, f"Sub{i}_base64.txt")
        for file_path in [filename, filename_base64]:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")

    # Define protocols and links
    protocols = ["vmess", "vless", "trojan", "ss", "ssr", "hy2", "tuic", "warp://"]
    links = [
        "https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt",
        "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
        "https://raw.githubusercontent.com/ts-sf/fly/main/v2",
        "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/app/sub.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_1.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_2.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_3.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_4.txt",
        "https://raw.githubusercontent.com/yebekhe/vpn-fail/refs/heads/main/sub-link",
        "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/mixed"
    ]
    dir_links = [
        "https://raw.githubusercontent.com/itsyebekhe/PSG/main/lite/subscriptions/xray/normal/mix",
        "https://raw.githubusercontent.com/HosseinKoofi/GO_V2rayCollector/main/mixed_iran.txt",
        "https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/refs/heads/main/mix/sub.html",
        "https://raw.githubusercontent.com/IranianCypherpunks/sub/main/config",
        "https://raw.githubusercontent.com/Rayan-Config/C-Sub/refs/heads/main/configs/proxy.txt",
        "https://raw.githubusercontent.com/sashalsk/V2Ray/main/V2Config",
        "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt",
        "https://raw.githubusercontent.com/itsyebekhe/HiN-VPN/main/subscription/normal/mix",
        "https://raw.githubusercontent.com/sarinaesmailzadeh/V2Hub/main/merged",
        "https://raw.githubusercontent.com/freev2rayconfig/V2RAY_SUBSCRIPTION_LINK/main/v2rayconfigs.txt",
        "https://raw.githubusercontent.com/Everyday-VPN/Everyday-VPN/main/subscription/main.txt",
        "https://raw.githubusercontent.com/C4ssif3r/V2ray-sub/main/all.txt",
        "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt",
    ]

    print("Fetching base64 encoded configs...")
    decoded_links = decode_links(links)
    print(f"Decoded {len(decoded_links)} base64 sources")
    
    print("Fetching direct text configs...")
    decoded_dir_links = decode_dir_links(dir_links)
    print(f"Decoded {len(decoded_dir_links)} direct text sources")

    print("Combining and filtering configs...")
    combined_data = decoded_links + decoded_dir_links
    merged_configs = filter_for_protocols(combined_data, protocols)
    print(f"Found {len(merged_configs)} unique configs after filtering")

    # Save to database
    Config.objects.all().delete()  # Clear previous configs
    for config in merged_configs:
        if config.strip() and not config.startswith('#'):
            protocol = config.split('://')[0]
            Config.objects.create(protocol=protocol, config_text=config)
    print("Configs saved to database!")

    # Write merged configs to output file
    print("Writing main config file...")
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(fixed_text)
        for config in merged_configs:
            f.write(config + "\n")
    print(f"Main config file created: {output_filename}")

    # Create base64 version of the main file
    print("Creating base64 version...")
    with open(output_filename, "r", encoding="utf-8") as f:
        main_config_data = f.read()
    
    with open(main_base64_filename, "w", encoding="utf-8") as f:
        encoded_main_config = base64.b64encode(main_config_data.encode()).decode()
        f.write(encoded_main_config)
    print(f"Base64 config file created: {main_base64_filename}")

    # Split configs by protocol (like sort.py)
    vmess = ""
    vless = ""
    trojan = ""
    ss = ""
    ssr = ""
    
    for config in merged_configs:
        if config.startswith("vmess"):
            vmess += config + "\n"
        elif config.startswith("vless"):
            vless += config + "\n"
        elif config.startswith("trojan"):
            trojan += config + "\n"
        elif config.startswith("ssr"):
            ssr += config + "\n"
        elif config.startswith("ss"):
            ss += config + "\n"

    # Write protocol-specific files
    protocol_files = {
        'vmess.txt': vmess,
        'vless.txt': vless,
        'trojan.txt': trojan,
        'ss.txt': ss,
        'ssr.txt': ssr
    }
    
    for filename, content in protocol_files.items():
        file_path = os.path.join(protocol_folder, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(fixed_text + content)
        print(f"Created: {file_path}")

    # Split merged configs into smaller files (no more than 500 configs per file)
    print("Creating split files...")
    num_lines = len(merged_configs)
    max_lines_per_file = 500
    num_files = (num_lines + max_lines_per_file - 1) // max_lines_per_file
    print(f"Splitting into {num_files} files with max {max_lines_per_file} lines each")

    for i in range(num_files):
        profile_title = f"🆓 Git:barry-far | Sub{i+1} 🔥"
        encoded_title = base64.b64encode(profile_title.encode()).decode()
        custom_fixed_text = f"""#profile-title: base64:{encoded_title}
#profile-update-interval: 1
#subscription-userinfo: upload=29; download=12; total=10737418240000000; expire=2546249531
#support-url: https://github.com/barry-far/V2ray-config
#profile-web-page-url: https://github.com/barry-far/V2ray-config
"""
        input_filename = os.path.join(output_folder, f"Sub{i + 1}.txt")
        with open(input_filename, "w", encoding="utf-8") as f:
            f.write(custom_fixed_text)
            start_index = i * max_lines_per_file
            end_index = min((i + 1) * max_lines_per_file, num_lines)
            for config in merged_configs[start_index:end_index]:
                f.write(config + "\n")
        print(f"Created: Sub{i + 1}.txt")

        with open(input_filename, "r", encoding="utf-8") as input_file:
            config_data = input_file.read()
        
        base64_output_filename = os.path.join(base64_folder, f"Sub{i + 1}_base64.txt")
        with open(base64_output_filename, "w", encoding="utf-8") as output_file:
            encoded_config = base64.b64encode(config_data.encode()).decode()
            output_file.write(encoded_config)
        print(f"Created: Sub{i + 1}_base64.txt")

    print(f"\nProcess completed successfully!")
    print(f"Total configs processed: {len(merged_configs)}")
    print(f"Files created:")
    print(f"  - All_Configs_Sub.txt")
    print(f"  - All_Configs_base64_Sub.txt")
    print(f"  - {num_files} split files (Sub1.txt to Sub{num_files}.txt)")
    print(f"  - {num_files} base64 split files (Sub1_base64.txt to Sub{num_files}_base64.txt)")