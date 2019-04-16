import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import datetime as dt


class Visualizer:
    def __init__(self):
        self.transaction_df = None
        with open("mint_subcategories", "r") as f:
            self.category_lookup = {i.split(",")[0].strip():i.split(",")[1].strip() for i in f.readlines()}
        self.subcategories = list(set(self.category_lookup.keys()))
        with open("mint_categories", "r") as f:
            self.categories = [i.strip() for i in f.readlines()]


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
        # Add main category label
        self.transaction_df["subcategory"] = self.transaction_df["Category"]
        self.transaction_df["Category"] = self.transaction_df["Category"].map(lambda x: self.category_lookup[x])


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
    
    
    def plot_transactions_for_month(self):
        return
    
    
    def plot_category_pie(self):
        if self.transaction_df is None:
            return
        
        labels = self.categories
        values = [len(self.transaction_df[self.transaction_df.Category==c]) for c in labels]
        trace = go.Pie(
            labels = labels,
            values = values,
            textinfo = "none"
        )
        
        layout = go.Layout(
            title = "Category Distribution"
        )
        
        fig = go.Figure(data=[trace], layout=layout)
        return fig

    
    def plot_explorer(self, start_date, end_date, accounts, transaction_types, categories, subcategories, merchants):
        if self.transaction_df is None:
            return
        
        # Limit transactions by date
        df = self.transaction_df[(self.transaction_df.Date >= start_date) & (self.transaction_df.Date <= end_date)]
        
        # Limit by account
        if accounts is not None:
            df = df[df["Account Name"].isin(accounts)]
        
        # Limit by transaction type
        df = df[df["Transaction Type"].isin(transaction_types)]
        
        # Limit by categories
        if categories is not None:
            df = df[df["Category"].isin(categories)]
        
        # Limit by subcategories
        if subcategories is not None:
            df = df[df["subcategory"].isin(subcategories)]
        
        # Limit by merchants
        if merchants is not None:
            df = df[df["subcategory"].isin(subcategories)]
        
        # Put credit as negative
        if "credit" in transaction_types:
            df["Amount"] = df.apply(lambda x: -x.Amount if x["Transaction Type"]=="credit" else x.Amount, axis=1)
        
        # Plot
        trace = go.Scatter(
            x = df.Date,
            y = df.Amount,
            text = df.Description,
            mode = "markers"
        )
        
        layout = go.Layout(
            title = "Transactions", 
            yaxis = dict(title="Charge Amount", hoverformat="$.2f"),
            xaxis = dict(title="Date"),
            hovermode = "closest"
        )
        
        fig = go.Figure(data=[trace], layout=layout)
        return fig
        
        
    def get_category_list(self):
        return self.categories
    
    
    def get_subcategory_list(self):
        return self.subcategories
    
    
    def get_accounts_list(self):
        if self.transaction_df is None:
            return None
        return self.transaction_df["Account Name"].unique()
    
    
    def get_merchant_list(self):
        if self.transaction_df is None:
            return None
        return self.transaction_df["Description"].unique()
    
    
    def get_date_range(self):
        if self.transaction_df is None:
            return None
        return self.transaction_df["Date"].min(), self.transaction_df["Date"].max()
        
        
if __name__ == "__main__":
    df = pd.read_csv("transactions.csv")
    visualizer = Visualizer()
    visualizer.set_transaction_data(df)
    #print(visualizer.transaction_df.columns)
    print(visualizer.plot_agreggate_transactions_by_month())
