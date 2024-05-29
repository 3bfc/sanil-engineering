import csv

plans_data = [[],[]]
collective_data = {}
for p in range(len(plans_data)):
  name = plans_data[p][0].split(' - ')[0]
  university = collective_data.get(name, 'N/A')
  plans_data[p][2] = university


