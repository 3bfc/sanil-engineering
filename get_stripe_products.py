import stripe

# Set your Stripe secret API key
stripe.api_key = 'sk_test_51OrkSkAgGoU5cz4B4uDGHP3yoLL3J6jtaggcEAMu54DlSxb3ul9ez2Hu0Fqs1GDiKHvjrvEZtOKwzy0aJSC0drbl00tp924MuE'

def get_all_products_and_prices():
    # Fetch all products
    products = stripe.Product.list(active=True, limit=100)
    
    for product in products.auto_paging_iter():
        print(f"******Product: {product['name']} ({product['id']})")
        
        # Fetch all prices for the current product
        prices = stripe.Price.list(product=product['id'], active=True, limit=100)
        
        for price in prices.auto_paging_iter():
            ms_price_id = price.get('metadata', {}).get('msPriceId', 'N/A')
            print(f"  Price ID: {price['id']} - Amount: {price['unit_amount']} {price['currency']} - msPriceId: {ms_price_id}")

if __name__ == "__main__":
    get_all_products_and_prices()