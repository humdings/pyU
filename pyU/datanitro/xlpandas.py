
import pandas as pd

from zipline.utils.factory import load_from_yahoo



def get_data(start,end, stocks):
    data = load_from_yahoo(
        indexes=None,
        stocks=stocks,
        start=start,
        end=end,
        adjusted=False
    )
    return data


def df_to_excel(cell, dataframe):
    #
    # DataNitro has Cell.df method that will do this.
    #
    # cell is either a tuple or Excel coord
    #
    anchor = Cell(cell)
    row, col = anchor.row, anchor.col
    idx = dataframe.index.values
    columns = dataframe.columns.values
    values = dataframe.values
    Cell(row, col+1).horizontal = columns
    Cell(row+1, col).vertical = idx
    Cell(row+1, col+1).table = [list(i) for i in values]

    autofit()


def to_df(cell, dt_index=False, utc=None):
    #
    # Extracts data from excel into a pandas DataFrame
    # There cant be any data below or to the right of the
    # being extracted.
    #
    anchor = Cell(cell)
    row, col = anchor.row, anchor.col
    idx = Cell(row+1, col).vertical
    columns = Cell(row, col+1).horizontal
    if dt_index:
        idx = pd.Index([pd.to_datetime(i, utc=utc) for i in idx])
    else:
        idx = pd.Index([i for i in idx])
    table = Cell(row+1, col+1).table
    return pd.DataFrame(table, index=idx, columns=columns)



    

    
