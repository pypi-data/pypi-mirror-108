from me_main_libs import *


def compute_performance_basic_portfolio(prices, portfolio_weights=None):
    returns = prices.pct_change().dropna()
    n_assets = len(prices.columns)
    if not portfolio_weights:
        portfolio_weights = n_assets * [1 / n_assets]

    portfolio_returns = pd.Series(np.dot(portfolio_weights, returns.T),
                                  index=returns.index)
    return portfolio_returns


def compute_needed_gain_to_restore_loss(percentage_loss=10):
    '''
    http://shurwest.com/wp-content/uploads/2013/08/The-Math-of-Gains-Losses.pdf
    As the loss gets bigger, the needed gain to restore the loss increases at an increasing rate. 
    '''
    result = (1/(1-percentage_loss/100))-1
    result = int(result*100)
    # result = f'{result}%'
    return result


def plot_needed_gain_to_restore_loss_relationship():
    results = {}
    for i in range(5, 80, 5):
        key = f'{-i}%'
        results[key] = compute_needed_gain_to_restore_loss(i)

    fig, ax = plt.subplots(1, 1)
    pd.Series(results).plot.bar(ax=ax)
    ax.set_ylabel('needed gain to restore loss (%)')
    ax.set_xlabel('percentage loss')
    plt.close()
    return fig
