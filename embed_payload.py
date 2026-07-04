import base64
import sys
import os

def main():
    print("Embedding payload stub into controller...")

    stub_path = 'dist/payload_stub.exe'
    if not os.path.exists(stub_path):
        print("❌ Error: dist/payload_stub.exe not found.")
        sys.exit(1)

    with open(stub_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    
    print(f"✅ Payload stub read. Base64 length: {len(b64)}")

    with open('controller.py', 'r', encoding='utf-8') as f:
        content = f.read()

    if 'PLACEHOLDER_BASE64_STRING' not in content:
        print("❌ Placeholder not found.")
        sys.exit(1)

    new_content = content.replace('PLACEHOLDER_BASE64_STRING', b64)

    with open('controller_embedded.py', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ controller_embedded.py created successfully.")

if __name__ == '__main__':
    main()