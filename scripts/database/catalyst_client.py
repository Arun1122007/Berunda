import requests

BASE_URL = "https://console.catalyst.zoho.in"
PROJECT_ID = "48591000000013025"

HEADERS = {
    "accept": "application/vnd.catalyst.v2+json",
    "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
    "catalyst-org": "60079736152",
    "cookie": "__Secure-iamsdt=0.CAESdBIwjvnBBCs93rpmu_n8n5CmVOcEu-DEGDQdPbPGscE8womn7CHvlGrV3FPAwKIJGKqWGkBPrJV2o5bh7Yy__kRJSTFomide2YD89xtdmS2IZcm0L-9yktsOFkaRZR1Vh0O94IyZXmu8owK6AFPglYWbDke6IJyT-6_5rs_HkwE; _iamadt=8ef9c1042b3ddeba66bbf9fc9f90a654e704bbe0c418341d3db3c6b1c13cc289a7ec21ef946ad5dc53c0c0a20918aa96; _iambdt=4fac9576a396e1ed8cbffe44494931689a275ed980fcf71b5d992d8865c9b42fef7292db0e164691651d558743bde08c995e6bbca302ba0053e095859b0e47ba; zps-tgr-dts=sc%3D1-expAppOnNewSession%3D%5B%5D-pc%3D1-sesst%3D1784815718526; ZohoMarkRef=\"https://catalyst.zoho.com/\"; ZohoMarkSrc=\"direct:catalyst|direct:catalyst|direct:catalyst\"; cookie-uid=\"\"; zalb_3a750b85f1=610d1a62042f6617b34189ea6e9f7ff8; ZD_CSRF_TOKEN=e8bb19d58bca676f4eeefa45c7127926006822724487cb10a7a1eaf079a0d836807d4762358079a15f5db0bc6a288e22d77e3dc01b1d3c566bf94b65b62edff4; JSESSIONID=19DA9507EA99A4A59F4F7ABA6604CA44; zalb_bc5826c95a=b74eadea9fd9b818d54644ef402cd382; CT_CSRF_TOKEN=e8bb19d58bca676f4eeefa45c7127926006822724487cb10a7a1eaf079a0d836807d4762358079a15f5db0bc6a288e22d77e3dc01b1d3c566bf94b65b62edff4; wms-tkp-token=60078390577-b7ef9b19-2b742e7b1e22b3930a8551b84eb267e1; zalb_zid=60079736152",
    "environment": "Development",
    "priority": "u=1, i",
    "project_id": "null",
    "referer": f"https://console.catalyst.zoho.in/baas/60079736152/project/{PROJECT_ID}/Development",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Microsoft Edge\";v=\"150\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
    "x-zcsrf-token": "zd_csrparam=e8bb19d58bca676f4eeefa45c7127926006822724487cb10a7a1eaf079a0d836807d4762358079a15f5db0bc6a288e22d77e3dc01b1d3c566bf94b65b62edff4"
}

def get_tables():
    url = f"{BASE_URL}/baas/v1/project/{PROJECT_ID}/table"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_table_columns(table_id):
    url = f"{BASE_URL}/baas/v1/project/{PROJECT_ID}/table/{table_id}/column"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("Fetching tables...")
    try:
        data = get_tables()
        print(f"Success! Found {len(data.get('data', []))} tables.")
    except Exception as e:
        print(f"Error: {e}")
