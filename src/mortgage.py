import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

MONTHLY = 12
BIWEEKLY = 24
WEEKLY = 52


def simulate(mortgage=475_000, interest=0.0286, payment=3500, savings=0, savings_return=0.07, t_f=30,
             frequency=MONTHLY):
    t_values = [0]
    mortgage_values = [mortgage]
    savings_values = [0]
    # 20 years
    # worst case stock market (6.4%): 1.947, 2.08
    # averages stock market (7%): 1.947, 2.228
    # best case stock market (18%): 5.068, 9.532
    # 30 years
    # worst case stock market (6%): 4.425
    # average case stock market (7%): 5.13, 6.141
    # best case stock market (8%):
    while t_values[-1] < t_f:
        current_time = t_values[-1]
        current_mortgage_principal = mortgage_values[-1]
        current_savings = savings_values[-1]

        if current_mortgage_principal > 0:
            interest_payment = interest * current_mortgage_principal / frequency  # biweekly
            principal_payment = payment - interest_payment
            savings_interest = current_savings * savings_return / frequency
            savings_payment = savings

            if principal_payment < 0:
                raise Exception('You will never pay off your mortgage!')
        else:
            principal_payment = 0
            savings_interest = current_savings * savings_return / frequency
            savings_payment = savings + payment

        t_values.append(current_time + 1 / frequency)
        mortgage_values.append(current_mortgage_principal - principal_payment)
        savings_values.append(current_savings + savings_interest + savings_payment)

    return np.array(t_values), np.array(mortgage_values), np.array(savings_values)


def simulate_graph(mortgage=475_000, interest=0.0286, payment=1728, savings=0, savings_return=0.07, t_f=20,
                   frequency=WEEKLY):
    t, mortgage, savings = simulate(mortgage=mortgage, interest=interest, payment=payment, savings=savings,
                                    savings_return=savings_return, t_f=t_f, frequency=frequency)
    print('Mortgage paid off after', t[np.argmax(-np.abs(mortgage))], 'years!')
    print('$', round(savings[-1] / 1e6, 3), 'million saved after', t_f, 'years!')
    plt.plot(t, mortgage / 1000, label='Mortgage Principal')
    plt.plot(t, savings / 1000, label='Savings')
    plt.xlabel('Time (years)')
    plt.ylabel('Money ($1000)')
    plt.legend()  # 2.8
    plt.show()


def vary_interest_graph(mortgage=351_000, interest=0.0286, t_f=20):
    stock_market_returns = np.linspace(0.04, 0.12, 1000)
    savings1 = np.array([simulate(mortgage=mortgage, interest=interest, payment=1700, savings=0, frequency=WEEKLY,
                                  savings_return=rate, t_f=t_f)[2][-1] for rate in stock_market_returns])
    savings2 = np.array([simulate(mortgage=mortgage, interest=interest, payment=700, savings=1000, frequency=WEEKLY,
                                  savings_return=rate, t_f=t_f)[2][-1] for rate in stock_market_returns])
    plt.plot(100 * stock_market_returns, savings1 / 1e6, label='Mortgage Paying')
    plt.plot(100 * stock_market_returns, savings2 / 1e6, label='Investing')
    plt.xlabel('Stock Market Annual Returns (%)')
    plt.ylabel('Savings in 20 years ($ Millions)')
    plt.ylim(0, np.max(savings2 / 1e6))
    plt.legend()
    plt.show()


if __name__ == '__main__':
    simulate_graph()
