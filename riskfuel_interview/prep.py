import numpy as np
import pandas as pd
from datetime import datetime

EPOCH = datetime.utcfromtimestamp(0)


def process():
    house_prices = pd.read_csv('kc_house_data.csv')
    house_prices = house_prices.drop(columns=['sqft_living'])  # this is a sum of sqft_living and sqft_above

    # 640k for 33 bedrooms makes no sense, and all other houses except for 1 have 11 or fewer rooms
    house_prices = house_prices.drop(house_prices[house_prices['bedrooms'] == 33].index)

    # houses with no bathrooms make no sense
    house_prices = house_prices.drop(house_prices[house_prices['bathrooms'] == 0].index)

    # format dates to seconds since EPOCH
    house_prices['date'] = house_prices['date'].map(lambda date:
                                                    (datetime.strptime(date[:-7], '%Y%m%d') - EPOCH).total_seconds())

    # dont care about these for linear fit because they have no absolute meaning
    house_prices = house_prices.drop(columns=['zipcode', 'lat', 'long'])

    # too nonlinear to work with
    house_prices = house_prices.drop(columns=['yr_renovated'])

    # don't think these matter
    house_prices = house_prices.drop(columns=['sqft_living15', 'sqft_lot15'])

    inputs = house_prices.drop(columns=['id', 'price'])
    inputs['b'] = np.ones(inputs.shape[0])
    output = house_prices['price']

    split = int(0.8 * inputs.shape[0])
    training_inputs = inputs[:split]
    training_outputs = output[:split]
    testing_inputs = inputs[split:]
    testing_outputs = output[split:]
    result = np.linalg.lstsq(training_inputs, training_outputs)
    factors = result[0]

    errors = np.dot(testing_inputs, factors) - testing_outputs

    print('Price Standard Deviation:', np.std(output))
    print('Mean Absolute Error:', np.mean(np.abs(errors)))


if __name__ == '__main__':
    process()
