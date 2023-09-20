import io
import base64
from django.shortcuts import render
from django.http import HttpResponse
import pickle
import numpy as np
import pandas as pd
import matplotlib.pylab as plt

# Create your views here.
def index(request):
    if request.method == 'POST':
        # Initialize a dictionary to store total wattages
        total_wattages = {}

        # print(request.POST.items())
        data = dict(request.POST)
        print(data)
        input_dict = {'House_Size_SqFt':0,
                      'Fan_Wattage':0,
                      'TV_Wattage':0,
                      'Washing_Machine_Wattage':0,
                      'Air_Conditioner_Wattage':0,
                      'Lighting_Wattage':0,
                      'Refrigerator_Wattage':0,
                      'Oven_Wattage':0,
                      'Microwave_Wattage':0,
                      'Toaster_Wattage':0,
                      'Dishwasher_Wattage':0,
                      'Coffee_Maker_Wattage':0,
                      'Computer_Wattage':0,
                      'Total_Electricity_Usage':0}
        
        # Iterate through POST data to collect appliance wattages
        for key, value in data.items():
            print(key, value)
            if key.startswith('House_Size_SqFt'):
                input_dict[key] = int(value[0])
            if key.startswith('appliance') and len(value) == 2:
                # print((key, value))

                appliance_name = value[0] # Extract appliance name from the key
                wattage = int(value[1])  # Convert the value to an integer



                # Add the wattage to the total for the corresponding appliance
                input_dict[appliance_name] = input_dict.get(appliance_name, 0) + wattage
        
        # Now, total_wattages contains the summed wattages for each appliance
        # You can access them like total_wattages['fan'], total_wattages['lighting'], etc.
        
        # You can perform further processing or calculations here

        print(input_dict)

        input_data = pd.DataFrame(input_dict,index=[1])

        estimated_price,efficiency_score = predict(input_data)

        plot_graph(input_dict)

        context = {
            'input_dict': input_dict,
            'estimated_price': estimated_price[0],
            'efficiency_score': efficiency_score[0]*100,
        }
        
        return render(request,'results.html',context)

    return render(request, 'index.html')


def predict(data):
    with open('decision_tree_model_price.pth','rb') as price_model_file:
        price_model = pickle.load(price_model_file)

    with open('decision_tree_model_score.pth','rb') as score_model_file:
        score_model = pickle.load(score_model_file)

    estimated_price = price_model.predict(data)
    efficiency_score = score_model.predict(data)
    print(estimated_price)
    print(efficiency_score)
    return estimated_price,efficiency_score


def plot_graph(data):

    averages = [111.14740174608941, 192.14442982053728, 466.97700285382086, 1223.8250739648995, 193.11268677787893, 157.62024194840063, 1693.501060027376, 740.3528120098447, 619.7483162773395, 1365.4402944828287, 729.4768824315674, 309.569539127357, 350.12139375396555]

    appliance_names = [key for key in data.keys() if key != 'House_Size_SqFt']
    wattages = [data[key] for key in appliance_names]

    # Create an array of indices for bar positioning
    x = np.arange(len(appliance_names))

    # Set the width of the bars
    width = 0.35

    # Create the figure and axes objects
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create the bars for user's data
    ax.bar(x - width/2, wattages, width, label='User')
    # Create the bars for averages data
    ax.bar(x + width/2, averages, width, label='Averages')

    # Set labels, title, and legend
    ax.set_xlabel('Appliances')
    ax.set_ylabel('Wattage')
    ax.set_title('Appliance wise electrical consumption (User vs. Averages)')
    ax.set_xticks(x)
    ax.set_xticklabels(appliance_names, rotation=45, ha='right')
    ax.legend()

    # Save the plot as an image file or display it
    plt.tight_layout()
    plt.savefig('static/plot.png')
    # plt.show()  # Uncomment this line to display the plot in a window

    # Close the plot
    plt.close()
    return None