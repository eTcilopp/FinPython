from models import Database, SRCalculations, Tickers
from  itertools import combinations 

def get_combinations(lst, portfolio_size):
    # Get all possible combinations of the list in groups of four
    all_combinations = combinations(lst, portfolio_size)
    for combination in all_combinations:
        # Check if there are any duplicates in the current combination
        if len(set(combination)) == 4:
            yield list(combination)


def run(portfolio_size, sharpe_ratio_threshold):
    tickers = session.query(Tickers.ticker).join(SRCalculations).filter(SRCalculations.asr > sharpe_ratio_threshold).all()
    tickers = [ticker[0] for ticker in tickers]
    for i in get_combinations(tickers, portfolio_size):
        print(i)

if __name__ == '__main__':
    db = Database("sqlite:///stocks_data.db")
    session = db.session    
    portfolio_size = 4
    sharpe_ratio_threshold = 1.2
    run(portfolio_size, sharpe_ratio_threshold)