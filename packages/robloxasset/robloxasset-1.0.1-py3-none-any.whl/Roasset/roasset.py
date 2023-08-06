import requests
class Asset:
    def asset_id(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['AssetId']
        return res
    def creator(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['Creator']['Name']
        return res
    def creator_id(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['Creator']['Id']
        return res
    def is_public(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['IsPublicDomain']
        return res
    def product_id(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['ProductId']
        return res
    def name(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['Name']
        return res
    def description(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['Description']
        return res
    def asset_type_id(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['AssetTypeId']
        return res
    def created_at(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['Created']
        return res
    def last_updated(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['Updated']
        return res
    def price_in_robux(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['PriceInRobux']
        return res
    def price_in_tickets(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['PriceInTickets']
        return res
    def sales(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['Sales']
        return res
    def is_new(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['IsNew']
        return res
    def is_for_sale(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['IsForSale']
        return res
    def is_limited(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['IsLimited']
        return res
    def remaining(id):
        url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(id)
        r = requests.get(url)
        res = r.json()['Remaining']
        return res
    def thumbnail(id):
        url = "https://www.roblox.com/Thumbs/Asset.ashx?width=110&height=110&assetId=" + str(id)
        r = requests.get(url, allow_redirects=True)
        return r.url
    def assetloc(id):
        url = "https://assetdelivery.roblox.com/v1/assetId/" + str(id)
        r = requests.get(url)
        res = r.json()['location']
        return res