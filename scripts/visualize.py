import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def update_charts(i):
    df = pd.read_csv('data/vega_vomma_data.csv')

    # Ensure the CSV contains the correct columns
    if 'CE_Vega' in df.columns and 'PE_Vega' in df.columns and 'CE_Vomma' in df.columns and 'PE_Vomma' in df.columns and 'Timestamp' in df.columns:
        call_vega = df.iloc[-1]['CE_Vega']
        call_vega = round(call_vega, 2)
        put_vega = df.iloc[-1]['PE_Vega']
        put_vega = round(put_vega, 2)

        x1 = df['Timestamp']
        y1_1 = df['CE_Vega']
        y1_2 = df['PE_Vega']

        plt.subplot(1, 2, 1)
        plt.plot(x1, y1_1, label='CE Vega')
        plt.plot(x1, y1_2, label='PE Vega')
        plt.xlabel('Time')
        plt.ylabel('Vega')
        plt.title(f'CE and PE VEGA TREND (CE Vega: {call_vega}, PE Vega: {put_vega})')
        plt.legend()

        call_v = df.iloc[-1]['CE_Vomma']
        call_v = round(call_v, 2)
        put_v = df.iloc[-1]['PE_Vomma']
        put_v = round(put_v, 2)

        x2 = df['Timestamp']
        y2_1 = df['CE_Vomma']
        y2_2 = df['PE_Vomma']

        plt.subplot(1, 2, 2)
        plt.plot(x2, y2_1, label='CE Vomma')
        plt.plot(x2, y2_2, label='PE Vomma')
        plt.xlabel('Time')
        plt.ylabel('Vomma')
        plt.title(f'CE and PE VOMMA (CE Vomma: {call_v}, PE Vomma: {put_v})')
        plt.legend()

        plt.tight_layout()

if __name__ == "__main__":
    ani = FuncAnimation(plt.gcf(), update_charts, interval=10000)
    plt.show()
