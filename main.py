from scripts.data_retrieval import DataRetriever
from scripts.vega_strategy import VegaStrategy
from scripts.report_generation import generate_report

def main():
    user_id = 'your_user_id'
    password = 'your_password'
    twofa = 'your_twofa'
    
    retriever = DataRetriever(user_id, password, twofa)
    strategy = VegaStrategy(retriever, '2024-06-27')
    
    try:
        strategy.run_strategy()
    except KeyboardInterrupt:
        generate_report()

if __name__ == "__main__":
    main()
