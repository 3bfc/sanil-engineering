import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import math
import re
# Load the CSV files
updated_plans_df = pd.read_csv('updated_plans.csv')
updated_plans_df = pd.read_csv('otc_repair.csv')
pricing_df = pd.read_csv('pricing.csv')

# Filter plans where is_filled is FALSE
plans_to_fill = updated_plans_df[updated_plans_df['is_filled'] == False]
plans = plans_to_fill
# Pricing details
otc_price = pricing_df[pricing_df['frequency'] == 'one time contribution']['price'].values
monthly_price = pricing_df[pricing_df['frequency'] == 'months']['price'].values
yearly_price = pricing_df[pricing_df['frequency'] == 'years']['price'].values

fields = [
  {
    "type": "PlainText",
    "displayName": "price"
  },
  {
    "type": "PlainText",
    "displayName": "price_id"
  },
  {
    "type": "PlainText",
    "displayName": "frequency"
  }
]
# Set up the WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox() for Firefox

# Replace with your Memberstack login URL and credentials
memberstack_url = 'https://app.memberstack.com/login'
username = 'rick@studentathletenil.com'
password = 'Avery123#'

driver.get(memberstack_url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)


def get_plan_ids():
  # Set up the WebDriver
  df = pd.read_csv('updated_plans.csv')
  filtered_df = df[df['plan_name'].str.contains('- OTC')]
  chunk = filtered_df.iloc[0:4]
  url = chunk.iloc[0]['url']
  driver = webdriver.Chrome()  # or webdriver.Firefox() for Firefox

  # Replace with your Memberstack login URL and credentials
  memberstack_url = 'https://app.memberstack.com/login'
  username = 'rick@studentathletenil.com'
  password = 'Avery123#'

  driver.get(memberstack_url)

  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(username)
  driver.find_element(By.NAME, "password").send_keys(password)
  driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
  
  for index, collective in filtered_df.iterrows():
    
    url = collective['url']
    cms = pd.DataFrame(columns=['name','price','price_id','frequency','checked','sort_value'])
    original_window = driver.current_window_handle
    col = collective['plan_name'].split(' - OTC')[0]
    print(f"****** {col} *******")
    frequency = "one time contribution"
    driver.get(url)
    time.sleep(10)
#   will need to do this per chunk
    p = driver.find_element(By.ID, "prices-header")
    if p.get_attribute('aria-expanded') == 'false':
      p.click()
    cards = driver.find_elements(By.CLASS_NAME, "Card-sc-16qsowb-0")
    for c in cards:
      print(c.text)
      price = c.find_element(By.CLASS_NAME,"lfkcIj").text.split(' USD')[0]
      
      name = f"{col} - {price} {frequency}"
      print(name)
      c.click()
      time.sleep(5)
      price_url = driver.current_url.split('/')
      price_id = price_url[len(price_url)-1]
      df.loc[len(df)] = {'name': name, 'price': price,'frequency':frequency,'price_id':'$$'}
      driver.get(url)
      time.sleep(5)
      # df = df.append([], ignore_index=True)
    cms.to_csv(f"SANIL {col}.csv",index=False)
    input("Save? Enter")
def signin():
  driver = webdriver.Chrome()  # or webdriver.Firefox() for Firefox

  # Replace with your Memberstack login URL and credentials
  memberstack_url = 'https://app.memberstack.com/login'
  username = 'rick@studentathletenil.com'
  password = 'Avery123#'

  driver.get(memberstack_url)

  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(username)
  driver.find_element(By.NAME, "password").send_keys(password)
  driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)


# THIS IS THE ONE
def other():
  df = pd.read_csv('updated_plans.csv')
  filtered_df = df[df['plan_name'].str.contains('- OTC')]

  for index, collective in filtered_df.iterrows():
      
      url = collective['url']
      cms = pd.DataFrame(columns=['name', 'price', 'price_id', 'frequency','sort_value','checked'])
      original_window = driver.current_window_handle
      col = collective['plan_name'].split(' - OTC')[0]
      print(f"****** {col} *******")
      
      driver.get(url)
      time.sleep(10)

      p = driver.find_element(By.ID, "prices-header")
      if p.get_attribute('aria-expanded') == 'false':
          p.click()
      
      # Refetch the cards inside the loop to avoid stale element reference
      cards = driver.find_elements(By.CLASS_NAME, "Card-sc-16qsowb-0")
      for i in range(len(cards)):
          # Refetch the cards to ensure they are up-to-date
          cards = driver.find_elements(By.CLASS_NAME, "Card-sc-16qsowb-0")
          card = cards[i]
          frequency = "one time contribution"
          
          try:
              input_string = card.find_element(By.CLASS_NAME, "lfkcIj").text
              # Extracting price
              price_match = re.search(r'\$([\d.]+)', input_string)
              price = float(price_match.group(1))

              # Extracting currency
              currency_match = re.search(r'(\w+) /', input_string)
              currency = currency_match.group(1)

              # Extracting interval
              interval_match = re.search(r'(\w+) /', input_string)
              frequency = interval_match.group(1)

              # Extracting only the numeric part of the price
              numeric_price = int(price)
              name = f"{col} - {price} per {frequency}"
              print(name)
              
              # Open a new tab using JavaScript
              driver.execute_script("window.open('');")
              
              # Switch to the new tab
              new_window = [window for window in driver.window_handles if window != original_window][0]
              driver.switch_to.window(new_window)
              
              # Click the card in the new tab
              driver.get(url)  # Navigate to the same URL in the new tab
              time.sleep(15)
              
              # Click the card again to navigate to the price page
              driver.find_elements(By.CLASS_NAME, "Card-sc-16qsowb-0")[i].click()
              
              time.sleep(5)
              
              # Get the price ID from the new tab
              price_url = driver.current_url.split('/')
              price_id = price_url[-1]
              
              # Close the new tab
              driver.close()
              
              # Switch back to the original tab
              driver.switch_to.window(original_window)
              
              # Append the data to the dataframe
              cms.loc[len(cms)] = {'name': f"{name}", 'price': f"{price}", 'frequency': f"per {frequency}", 'price_id': price_id,'sort_value':numeric_price,'checked':''}
              print(price_id)
              # Reload the original URL to reset the state
              driver.get(url)
              time.sleep(5)
          
          except StaleElementReferenceException:
              print("StaleElementReferenceException caught. Skipping this element.")
              continue
      cms.to_csv(f"SANIL {col} {frequency}.csv", index=False)




def delete_bad_prices(plan_url):
  driver.get(plan_url)
  time.sleep(5)
  p = driver.find_element(By.ID, "prices-header").click()
  cards = driver.find_elements(By.CLASS_NAME, "Card-sc-16qsowb-0")
  for c in cards:
    print(c)
    c.find_element(By.CLASS_NAME,"grGwvJ").click()
    time.sleep(2)
    c.find_element(By.CLASS_NAME,"bOmncY").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "[type=submit").click()
    time.sleep(2)

def run_removal():
    for index, plan in plans.iterrows():
      plan_name = plan['plan_name']
      print(plan_name)
      uni = plan['university']
      url = f"{plan['url']}"
      driver.get(url)
      time.sleep(5)
      p = driver.find_element(By.ID, "prices-header")
      if p.get_attribute('aria-expanded') == 'false':
        p.click()
      cards = driver.find_elements(By.CLASS_NAME, "Card-sc-16qsowb-0")
      for c in range(len(cards)):
        print(c)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "grGwvJ")))
        element.click()
        # cards[c].find_element(By.CLASS_NAME,"grGwvJ").click()
        time.sleep(2)
        cards[c].find_element(By.CLASS_NAME,"bOmncY").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "[type=submit").click()
        time.sleep(2)


def fill_form(driver, plan_name, uni, price, frequency):
  # Locate and clear the input fields
  print(plan_name)
  
  # change name 
  name = driver.find_element(By.NAME, "name")
  name.send_keys(f"{uni} - {price} {frequency}")

  # check if otc
  if frequency == 'one time contribution':
    # otc = driver.find_element(By.CLASS_NAME,"eQQCtj")
    otc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "eQQCtj")))
    otc.click()

  # change price


  amount_input = driver.find_element(By.NAME, "amount")
  amount_input.send_keys(Keys.COMMAND + "a")
  amount_input.send_keys(Keys.DELETE)
  amount_input.send_keys(price)

  # change recurring frequency
  if frequency == 'years':
    select_list = driver.find_elements(By.CLASS_NAME, 'css-dx4opd-control')
    select_list[1].click()

    c = 'css-tiil3y-menu'
    menu = driver.find_element(By.CLASS_NAME,c)

    z = menu.find_element(By.CSS_SELECTOR,'[aria-label=years]')
    
    z.click()
  
  # Submit the form
  btn = driver.find_element(By.CLASS_NAME, "kEUoiQ")
  btn.click()

  submit = driver.find_element(By.CSS_SELECTOR,"[type=submit]")
  submit.click()
  time.sleep(15)
def test():
    plan_name = plan['plan_name']
    uni = plan['university']
    # #####
    url = f"{plan['url']}/create-price"
    for price in otc_price:
      # Navigate to the URL
      driver.get(url)
      time.sleep(5)
      # Locate and clear the input fields

      
      # change name 
      name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "name")))
      z = f"{uni} - {price} {frequency}"
      name.send_keys(z)
      print(z)
      time.sleep(2)
      otc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "eQQCtj")))
      print(otc.text)
      if otc.text == 'One-time':
        otc.click()
        # otc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ijJPtr")))

      time.sleep(2)
      amount_input = driver.find_element(By.NAME, "amount")
      amount_input.send_keys(Keys.COMMAND + "a")
      amount_input.send_keys(Keys.DELETE)
      amount_input.send_keys(price)

      # Submit the form
      btn = driver.find_element(By.CLASS_NAME, "kEUoiQ")
      btn.click()

      submit = driver.find_element(By.CSS_SELECTOR,"[type=submit]")
      submit.click()
      time.sleep(5)

    # input("Press Enter to continue to the next plan...")
    updated_plans_df.at[index, 'is_filled'] = True

try:
  # Iterate through each plan
  now = datetime.now()

  # Format the timestamp
  formatted_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

  # Print the formatted timestamp
  print(formatted_timestamp)
  frequency = "one time contribution"
  for index, plan in plans_to_fill.iterrows():
    plan_name = plan['plan_name']
    uni = plan['university']
    # #####
    url = f"{plan['url']}/create-price"
    for price in otc_price:
      # Navigate to the URL
      driver.get(url)
      time.sleep(5)
      # Locate and clear the input fields
      print(plan_name)
      
      # change name 
      name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "name")))
      z = f"{uni} - {price} {frequency}"
      name.send_keys(z)
      print(z)
      time.sleep(4)
      otc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "eQQCtj")))
      if otc.text == 'One-time':
        otc.click()
        # otc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ijJPtr")))

      time.sleep(3)
      amount_input = driver.find_element(By.NAME, "amount")
      amount_input.send_keys(Keys.COMMAND + "a")
      amount_input.send_keys(Keys.DELETE)
      amount_input.send_keys(price)

      # Submit the form
      btn = driver.find_element(By.CLASS_NAME, "kEUoiQ")
      btn.click()

      submit = driver.find_element(By.CSS_SELECTOR,"[type=submit]")
      submit.click()
      time.sleep(10)

    # input("Press Enter to continue to the next plan...")
    updated_plans_df.at[index, 'is_filled'] = True
    # #########
    # Determine the pricing to use
    if "- OTC" in plan_name:
      for price in otc_price:
        # Navigate to the URL
        driver.get(url)
        time.sleep(15)
        fill_form(driver, plan_name, uni, price, 'one time contribution')
    else:
      for price in monthly_price:
        driver.get(url)
        time.sleep(15)
        fill_form(driver, plan_name, uni, price, 'months')
      for price in yearly_price:
        driver.get(url)
        time.sleep(15)
        fill_form(driver, plan_name, uni, price, 'years')
    # Wait for a short period to ensure form submission is processed
    updated_plans_df.at[index, 'is_filled'] = True

finally:
  print("done!")
  now = datetime.now()

  # Format the timestamp
  formatted_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

  # Print the formatted timestamp
  print(formatted_timestamp)
  updated_plans_df.to_csv('updated_plans.csv', index=False)
  





