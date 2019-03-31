import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import datetime as dt


class Visualizer:
    def __init__(self):
        self.transaction_df = None
        return


    def set_transaction_data(self, transactions_df):
        """
        Sets the transaction data

        transactions : Pandas dataframe from Utility parse_content. From a Mint CSV.
        """
        self.transaction_df = transactions_df
        # Fix dates "3/28/2019"
        self.transaction_df["Date"] = self.transaction_df["Date"].map(lambda x: dt.datetime.strptime(x, "%m/%d/%Y"))
        # Add month info
        self.transaction_df["month"] = self.transaction_df["Date"].map(lambda x: dt.date(x.year, x.month, 1))


    def plot_agreggate_transactions_by_month(self):
        if self.transaction_df is None:
            return

        traces = []
        for account, df in self.transaction_df.groupby("Account Name"):
            data = df.groupby("month").Date.count()
            trace = go.Bar(
                x = data.index,
                y = data,
                name = account
            )
            traces.append(trace)

        layout = go.Layout(
            title = "Total Number of Transactions",
            barmode = "stack",
            xaxis = dict(title="Month"),
            yaxis = dict(title="Number of Transactions")
        )
        fig = go.Figure(data=traces, layout=layout)
        return fig


if __name__ == "__main__":
    df = pd.read_csv("transactions.csv")
    visualizer = Visualizer()
    visualizer.set_transaction_data(df)
    #print(visualizer.transaction_df.columns)
    print(visualizer.plot_agreggate_transactions_by_month())
